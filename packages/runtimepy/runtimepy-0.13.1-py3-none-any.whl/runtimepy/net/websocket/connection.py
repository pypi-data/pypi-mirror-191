"""
A module implementing a WebSocket connection interface.
"""

from __future__ import annotations

# built-in
from contextlib import asynccontextmanager as _asynccontextmanager
from typing import AsyncIterator as _AsyncIterator
from typing import Awaitable as _Awaitable
from typing import Callable as _Callable
from typing import Optional as _Optional
from typing import Tuple as _Tuple
from typing import Type as _Type
from typing import TypeVar as _TypeVar
from typing import Union as _Union

# third-party
import websockets
from websockets.client import (
    WebSocketClientProtocol as _WebSocketClientProtocol,
)
from websockets.exceptions import ConnectionClosed as _ConnectionClosed
from websockets.server import (
    WebSocketServerProtocol as _WebSocketServerProtocol,
)
from websockets.server import WebSocketServer as _WebSocketServer
from websockets.server import serve as _serve

# internal
from runtimepy.net.connection import BinaryMessage, Connection

T = _TypeVar("T", bound="WebsocketConnection")
ConnectionInit = _Callable[[T], _Awaitable[bool]]
V = _TypeVar("V")


class WebsocketConnection(Connection):
    """A simple websocket connection interface."""

    def __init__(
        self,
        protocol: _Union[_WebSocketClientProtocol, _WebSocketServerProtocol],
    ) -> None:
        """Initialize this connection."""

        self.protocol = protocol
        super().__init__(self.protocol.logger)

    async def _handle_connection_closed(
        self, task: _Awaitable[V]
    ) -> _Optional[V]:
        """A wrapper for handling connection close."""

        result = None
        try:
            result = await task
        except _ConnectionClosed:
            self.disable("connection closed")
        return result

    async def _await_message(self) -> _Optional[_Union[BinaryMessage, str]]:
        """Await the next message. Return None on error or failure."""
        return await self._handle_connection_closed(self.protocol.recv())

    async def _send_text_message(self, data: str) -> None:
        """Send a text message."""
        await self._handle_connection_closed(self.protocol.send(data))

    async def _send_binay_message(self, data: BinaryMessage) -> None:
        """Send a binary message."""
        await self._handle_connection_closed(self.protocol.send(data))

    async def close(self) -> None:
        """Close this connection."""
        await self.protocol.close()

    @classmethod
    @_asynccontextmanager
    async def client(cls: _Type[T], uri: str) -> _AsyncIterator[T]:
        """A wrapper for connecting a client."""

        async with getattr(websockets, "connect")(uri) as protocol:
            client = cls(protocol)
            yield client

    @classmethod
    def server_handler(
        cls: _Type[T], init: ConnectionInit[T]
    ) -> _Callable[[_WebSocketServerProtocol], _Awaitable[None]]:
        """
        A wrapper for passing in a websocket handler and initializing a
        connection.
        """

        async def _handler(protocol: _WebSocketServerProtocol) -> None:
            """A handler that runs the callers initialization function."""
            conn = cls(protocol)
            if await init(conn):
                await conn.process()

        return _handler

    @classmethod
    @_asynccontextmanager
    async def create_pair(cls: _Type[T]) -> _AsyncIterator[_Tuple[T, T]]:
        """Obtain a connected pair of WebsocketConnection objects."""

        server_conn: _Optional[T] = None

        async def server_init(protocol: _WebSocketServerProtocol) -> bool:
            """Create one side of the connection and update the reference."""
            nonlocal server_conn
            assert server_conn is None
            server_conn = cls(protocol)
            return True

        # Start a server.
        async with _serve(server_init, host="0.0.0.0", port=0) as server:
            host = list(server.sockets)[0].getsockname()

            # Connect a client and yield both sides of the connection.
            async with cls.client(f"ws://localhost:{host[1]}") as client_conn:
                assert server_conn is not None
                yield server_conn, client_conn

    @classmethod
    @_asynccontextmanager
    async def serve(
        cls: _Type[T], init: ConnectionInit[T], **kwargs
    ) -> _AsyncIterator[_WebSocketServer]:
        """Serve a WebSocket server."""

        async with _serve(cls.server_handler(init), **kwargs) as server:
            yield server
