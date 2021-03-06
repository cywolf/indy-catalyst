"""Ping handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ..messages.ping import Ping
from ..messages.ping_response import PingResponse
from ....models.thread_decorator import ThreadDecorator


class PingHandler(BaseHandler):
    """Ping handler class."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle ping message.

        Args:
            context: Request context
            responder: Responder used to reply

        """
        self._logger.debug(f"PingHandler called with context {context}")
        assert isinstance(context.message, Ping)

        self._logger.info("Received trust ping from: %s", context.sender_did)

        if not context.connection_active:
            self._logger.info(
                "Connection not active, skipping ping response: %s", context.sender_did
            )
            return

        if context.message.response_requested:
            reply = PingResponse(_thread=ThreadDecorator(thid=context.message._id))
            await responder.send_reply(reply)
