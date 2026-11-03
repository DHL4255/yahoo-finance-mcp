"""Run yahoo_finance_mcp.py as a remote MCP server (Streamable HTTP).

Settings come from environment variables:
  PORT      port to listen on (cloud hosts set this for you)
  MCP_PATH  secret URL path, e.g. /mcp-7f3c9a... (acts as the access key)
"""
import os

from mcp.server.transport_security import TransportSecuritySettings

import yahoo_finance_mcp as yfm

mcp = yfm.mcp
mcp.settings.host = "0.0.0.0"
mcp.settings.port = int(os.environ.get("PORT", "8000"))
mcp.settings.stateless_http = True
mcp.settings.streamable_http_path = os.environ["MCP_PATH"]

# DNS-rebinding protection guards servers on a private network against
# malicious web pages. This server is public by design, so the check only
# risks rejecting legitimate requests that arrive through the host's proxy.
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False
)


# Public, harmless endpoint for wake-up pings and health checks.
# It returns "ok" and exposes no tools, so it doesn't reveal the secret path.
from starlette.requests import Request
from starlette.responses import PlainTextResponse


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> PlainTextResponse:
    return PlainTextResponse("ok")


mcp.run(transport="streamable-http")
