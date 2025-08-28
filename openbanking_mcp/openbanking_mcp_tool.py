from openbanking_client import OpenBankingClient

from openbanking_config import APP_ID, KEY_PATH, REDIRECT_URL

client = OpenBankingClient(APP_ID, KEY_PATH, REDIRECT_URL)


def fetch_accounts():
    """Start OAuth authorization flow to get accounts."""
    try:
        token = client.build_jwt()
        consent_url = client.start_authorization(token)

        return {
            "status": "authorization_required",
            "message": "OAuth authorization required to access accounts",
            "consent_url": consent_url,
            "instructions": "Please visit the consent URL to authorize access, then provide the authorization code",
        }
    except Exception as e:
        return {"error": str(e)}


def complete_authorization(authorization_code: str):
    """Complete OAuth flow by exchanging authorization code for accounts."""
    try:
        token = client.build_jwt()
        session = client.exchange_code_for_session(token, authorization_code)
        accounts = session.get("accounts", [])

        return {
            "status": "success",
            "accounts": accounts,
            "message": f"Successfully retrieved {len(accounts)} accounts",
        }
    except Exception as e:
        return {"error": str(e)}


def fetch_transactions(account_uid: str):
    token = client.build_jwt()
    return client.get_transactions(token, account_uid)
