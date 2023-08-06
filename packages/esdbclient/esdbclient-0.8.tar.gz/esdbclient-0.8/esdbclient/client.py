# -*- coding: utf-8 -*-
import re
import sys
from typing import Iterable, Iterator, Optional, Sequence, Tuple, Union

import grpc
from grpc import RpcError

from esdbclient.esdbapi import (
    BasicAuthCallCredentials,
    Streams,
    SubscriptionReadRequest,
    SubscriptionReadResponse,
    Subscriptions,
    handle_rpc_error,
)
from esdbclient.events import NewEvent, RecordedEvent
from esdbclient.exceptions import StreamNotFound

ESDB_EVENTS_REGEX = "\\$.*"  # Matches the 'type' of system events.


class EsdbClient:
    """
    Encapsulates the EventStoreDB gRPC API.
    """

    def __init__(
        self,
        uri: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        server_cert: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        # Todo: look at connection string for "tls=true" or "tls=false"

        if isinstance(uri, (str, bytes)) and re.match(pattern=r"^\w+:\d+$", string=uri):
            self.grpc_target = uri
        elif host is not None:
            assert port is not None
            self.grpc_target = f"{host}:{port}"
        else:
            raise ValueError("Invalid constructor args")
        if server_cert is None:
            self._channel = grpc.insecure_channel(target=self.grpc_target)
            self._call_credentials = None
        else:
            assert username is not None
            assert password is not None
            channel_credentials = grpc.ssl_channel_credentials(
                root_certificates=server_cert.encode()
            )
            self._channel = grpc.secure_channel(
                target=self.grpc_target, credentials=channel_credentials
            )
            self._call_credentials = grpc.metadata_call_credentials(
                BasicAuthCallCredentials(username, password)
            )
        self._streams = Streams(self._channel)
        self._subscriptions = Subscriptions(self._channel)

    def append_events(
        self,
        stream_name: str,
        expected_position: Optional[int],
        events: Iterable[NewEvent],
        timeout: Optional[float] = None,
    ) -> int:
        """
        Appends new events to the named stream.
        """
        return self._streams.append(
            stream_name=stream_name,
            expected_position=expected_position,
            events=events,
            timeout=timeout,
        )

    def read_stream_events(
        self,
        stream_name: str,
        position: Optional[int] = None,
        backwards: bool = False,
        limit: int = sys.maxsize,
        timeout: Optional[float] = None,
    ) -> Iterable[RecordedEvent]:
        """
        Reads recorded events from the named stream.
        """
        return self._streams.read(
            stream_name=stream_name,
            stream_position=position,
            backwards=backwards,
            limit=limit,
            timeout=timeout,
            credentials=self._call_credentials,
        )

    def read_all_events(
        self,
        commit_position: Optional[int] = None,
        backwards: bool = False,
        filter_exclude: Sequence[str] = (ESDB_EVENTS_REGEX,),
        filter_include: Sequence[str] = (),
        limit: int = sys.maxsize,
        timeout: Optional[float] = None,
    ) -> Iterable[RecordedEvent]:
        """
        Reads recorded events in "all streams" in the database.
        """
        return self._streams.read(
            commit_position=commit_position,
            backwards=backwards,
            filter_exclude=filter_exclude,
            filter_include=filter_include,
            limit=limit,
            timeout=timeout,
            credentials=self._call_credentials,
        )

    def get_stream_position(
        self,
        stream_name: str,
        timeout: Optional[float] = None,
    ) -> Optional[int]:
        """
        Returns the current position of the end of a stream.
        """
        try:
            last_event = list(
                self._streams.read(
                    stream_name=stream_name,
                    backwards=True,
                    limit=1,
                    timeout=timeout,
                    credentials=self._call_credentials,
                )
            )[0]
        except StreamNotFound:
            return None
        else:
            return last_event.stream_position

    def get_commit_position(
        self,
        timeout: Optional[float] = None,
        filter_exclude: Sequence[str] = (ESDB_EVENTS_REGEX,),
    ) -> int:
        """
        Returns the current commit position of the database.
        """
        recorded_events = self.read_all_events(
            backwards=True,
            filter_exclude=filter_exclude,
            limit=1,
            timeout=timeout,
        )
        commit_position = 0
        for ev in recorded_events:
            commit_position = ev.commit_position
        return commit_position

    def subscribe_all_events(
        self,
        commit_position: Optional[int] = None,
        filter_exclude: Sequence[str] = (ESDB_EVENTS_REGEX,),
        filter_include: Sequence[str] = (),
        timeout: Optional[float] = None,
    ) -> Iterator[RecordedEvent]:
        """
        Returns a catch-up subscription, from which recorded
        events in "all streams" in the database can be received.
        """
        read_resp = self._streams.read(
            commit_position=commit_position,
            filter_exclude=filter_exclude,
            filter_include=filter_include,
            subscribe=True,
            timeout=timeout,
            credentials=self._call_credentials,
        )
        return CatchupSubscription(read_resp=read_resp)

    def create_subscription(
        self,
        group_name: str,
        from_end: bool = False,
        commit_position: Optional[int] = None,
        # filter_exclude: Sequence[str] = (ESDB_EVENTS_REGEX,),
        filter_exclude: Sequence[str] = (),
        filter_include: Sequence[str] = (),
        timeout: Optional[float] = None,
    ) -> None:
        self._subscriptions.create(
            group_name=group_name,
            from_end=from_end,
            commit_position=commit_position,
            filter_exclude=filter_exclude,
            filter_include=filter_include,
            timeout=timeout,
            credentials=self._call_credentials,
        )

    def read_subscription(
        self, group_name: str, timeout: Optional[float] = None
    ) -> Tuple[SubscriptionReadRequest, SubscriptionReadResponse]:
        return self._subscriptions.read(
            group_name=group_name,
            timeout=timeout,
            credentials=self._call_credentials,
        )


class CatchupSubscription(Iterator[RecordedEvent]):
    """
    Encapsulates read response for a catch-up subscription.
    """

    def __init__(
        self,
        read_resp: Iterable[RecordedEvent],
    ):
        self.read_resp = iter(read_resp)

    def __iter__(self) -> Iterator[RecordedEvent]:
        return self

    def __next__(self) -> RecordedEvent:
        try:
            return next(self.read_resp)
        except RpcError as e:
            raise handle_rpc_error(e) from e  # pragma: no cover
