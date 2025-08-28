#!/usr/bin/env python3
import asyncio
from mcp.server.fastmcp import FastMCP
from openbanking_mcp_tool import (
    fetch_transactions,
    fetch_accounts,
    complete_authorization,
)

# Initialize the MCP server
server = FastMCP("openbanking-agent")


# Tool to start OAuth authorization for accounts
@server.tool()
async def fetch_accounts_tool(**kwargs):
    """Start OAuth authorization flow to get accounts."""
    try:
        result = fetch_accounts()
        return result
    except Exception as e:
        return {"error": str(e)}


# Tool to complete OAuth authorization
@server.tool()
async def complete_authorization_tool(authorization_code: str, **kwargs):
    """Complete OAuth flow by exchanging authorization code for accounts."""
    try:
        result = complete_authorization(authorization_code)
        return result
    except Exception as e:
        return {"error": str(e)}


# Tool to fetch transactions
@server.tool()
async def fetch_transactions_tool(account_uid: str, **kwargs):
    """Fetch transactions for a given account."""
    try:
        transactions = fetch_transactions(account_uid)
        return {"transactions": transactions}
    except Exception as e:
        return {"error": str(e)}


def run():
    """Run the server - this is what mcp run expects"""
    return asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    # Run the server
    print("🔍 Starting Open Banking MCP Server...")
    run()
