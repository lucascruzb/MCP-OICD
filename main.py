import os
from fastmcp.server import FastMCP, create_proxy
from fastmcp.server.auth.oidc_proxy import OIDCProxy
import logging

logging.basicConfig(level=logging.DEBUG)

logging.getLogger("fastmcp").setLevel(logging.DEBUG)
logging.getLogger("mcp").setLevel(logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)
logging.getLogger("httpcore").setLevel(logging.DEBUG)

auth = OIDCProxy(
    config_url=os.environ.get("AUTH0_CONFIG_URL"),
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    base_url=os.environ.get("BASE_URL", "https://localhost:8000"),
    required_scopes= [
    "openid",
    "profile",
    "email",
    "offline_access"
  ]
    )

config = {
    "mcpServers": {
        "wazuh": {
            "url": "http://10.1.0.10:3000/mcp",
            "transport": "http"
        },
        "thehive": {
            "url": "http://10.1.0.11:8082/mcp",
            "transport": "http"
        }
    }
}

mcp = create_proxy(config, auth=auth, name="SOC-Gateway")

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )