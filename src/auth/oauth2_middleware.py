import json
import os

from a2a.types import AgentCard

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse


class OAuth2Middleware(BaseHTTPMiddleware):
    """Starlette middleware that authenticates A2A access using an OAuth2 bearer token."""

    def __init__(
        self,
        app: Starlette,
        agent_card: AgentCard = None,
        public_paths: list[str] = None,
    ):
        super().__init__(app)
        self.agent_card = agent_card
        self.public_paths = set(public_paths or [])
        self.a2a_auth = False

        for key, _ in agent_card.security_schemes.items():
            if key == "apiKey":
                self.a2a_auth = True

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # Allow public paths and anonymous access
        if path in self.public_paths or not self.a2a_auth:
            return await call_next(request)

        # Authenticate the request
        auth_header = request.headers.get('apiKey')
        print(f" auth_header: {auth_header}")
        if not auth_header:
            return self._unauthorized(
                'Missing or malformed Authorization header.', request
            )

        try:
            if self.a2a_auth:
                if auth_header in ["12345", "abcd"]:
                    print("access token is valid")
                else:
                    return self._forbidden(
                        f'Invalid token', request
                    )
        except Exception as e:
            return self._forbidden(f'Authentication failed: {e}', request)
        return await call_next(request)

    def _forbidden(self, reason: str, request: Request):
        accept_header = request.headers.get('accept', '')
        if 'text/event-stream' in accept_header:
            return PlainTextResponse(
                f'error forbidden: {reason}',
                status_code=403,
                media_type='text/event-stream',
            )
        return JSONResponse(
            {'error': 'forbidden', 'reason': reason}, status_code=403
        )

    def _unauthorized(self, reason: str, request: Request):
        accept_header = request.headers.get('accept', '')
        if 'text/event-stream' in accept_header:
            return PlainTextResponse(
                f'error unauthorized: {reason}',
                status_code=401,
                media_type='text/event-stream',
            )
        return JSONResponse(
            {'error': 'unauthorized', 'reason': reason}, status_code=401
        )
