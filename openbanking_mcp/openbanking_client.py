import time
import jwt
import requests
from pathlib import Path
from openbanking_config import API, APP_ID, KEY_PATH, REDIRECT_URL


class OpenBankingClient:
    def __init__(self, app_id: str, key_path: str, redirect_url: str):
        self.app_id = app_id
        self.key_path = key_path
        self.redirect_url = redirect_url
        self.api = "https://api.enablebanking.com"

    def build_jwt(self) -> str:
        """Build RS256 JWT token for API authentication."""
        key = Path(self.key_path).read_bytes()
        now = int(time.time())
        return jwt.encode(
            {
                "iss": "enablebanking.com",
                "aud": "api.enablebanking.com",
                "iat": now,
                "exp": now + 3600,
            },
            key,
            algorithm="RS256",
            headers={"kid": self.app_id},
        )

    def start_authorization(self, token: str) -> str:
        """Initiate authorization with Mock ASPSP and return consent URL."""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        body = {
            "access": {"valid_until": "2025-12-31T00:00:00Z"},
            "aspsp": {"name": "Mock ASPSP", "country": "FI"},
            "state": "demo-state",
            "redirect_url": REDIRECT_URL,
            "psu_type": "personal",
        }
        resp = requests.post(f"{API}/auth", headers=headers, json=body, timeout=60)
        resp.raise_for_status()
        return resp.json()["url"]

    def exchange_code_for_session(self, token: str, code: str) -> dict:
        """Exchange code for session and return session data."""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            f"{API}/sessions", headers=headers, json={"code": code}, timeout=60
        )
        resp.raise_for_status()
        return resp.json()

    def get_transactions(self, token: str, account_uid: str) -> list:
        """Fetch transactions for a given account, handling pagination."""
        headers = {"Authorization": f"Bearer {token}"}
        all_tx, params = [], {}

        while True:
            resp = requests.get(
                f"{API}/accounts/{account_uid}/transactions",
                headers=headers,
                params=params,
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()

            tx = data.get("transactions", data.get("booked", []))
            if not isinstance(tx, list):
                tx = []
            all_tx.extend(tx)

            continuation_key = data.get("continuation_key")
            if not continuation_key:
                break
            params = {"continuation_key": continuation_key}

        return all_tx

    def sanity_check_jwt(self, token: str):
        test = requests.get(
            f"{API}/aspsps", headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        print("ASPSPs status:", test.status_code, test.text)


def main():
    print("🔑 Generating token...")
    client = OpenBankingClient(APP_ID, KEY_PATH, REDIRECT_URL)
    token = client.build_jwt()

    print("\n🌐 Starting authorization with Mock ASPSP...")
    consent_url = client.start_authorization(token)
    print(f"Open this URL and approve access:\n{consent_url}")

    code = input("\nPaste code here: ").strip()

    print("\n📄 Exchanging code for session...")
    session = client.exchange_code_for_session(token, code)
    accounts = session.get("accounts") or []

    if not accounts:
        print("⚠️ No accounts found. Check Mock ASPSP panel.")
        return

    print("\n✅ Accounts:")
    for account in accounts:
        print(account)

    account_uid = accounts[0]["uid"] if isinstance(accounts[0], dict) else accounts[0]

    print("\n💳 Fetching transactions...")
    transactions = client.get_transactions(token, account_uid)

    print(f"\n📊 Total transactions: {len(transactions)}. Showing up to 5:")
    for tx in transactions:
        print(tx)


if __name__ == "__main__":
    main()
