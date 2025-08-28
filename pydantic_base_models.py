from pydantic import BaseModel, Field
from typing import List, Optional


# For the accounts response
class AccountInfo(BaseModel):
    account_id: str = Field(description="Unique account identifier")
    account_name: str = Field(description="Name of the account")
    currency: str = Field(description="Account currency")
    balance: Optional[float] = Field(description="Current account balance")


class AccountsResponse(BaseModel):
    status: str = Field(description="Response status")
    message: Optional[str] = Field(description="Response message")
    consent_url: Optional[str] = Field(
        description="OAuth consent URL if authorization required"
    )
    accounts: Optional[List[AccountInfo]] = Field(
        description="List of accounts if available"
    )
    error: Optional[str] = Field(description="Error message if any")


# For transactions
class TransactionAmount(BaseModel):
    currency: str = Field(description="Transaction currency")
    amount: str = Field(description="Transaction amount")


class TransactionParty(BaseModel):
    name: str = Field(description="Name of the party")
    postal_address: Optional[str] = Field(description="Postal address")
    organisation_id: Optional[str] = Field(description="Organization ID")


class Transaction(BaseModel):
    entry_reference: str = Field(description="Transaction reference")
    merchant_category_code: Optional[str] = Field(description="Merchant category code")
    transaction_amount: TransactionAmount
    creditor: Optional[TransactionParty] = Field(description="Creditor information")
    debtor: Optional[TransactionParty] = Field(description="Debtor information")
    booking_date: Optional[str] = Field(description="Booking date")
    value_date: Optional[str] = Field(description="Value date")
    description: Optional[str] = Field(description="Transaction description")


class TransactionList(BaseModel):
    transactions: List[Transaction] = Field(description="List of transactions")


# For OAuth completion
class OAuthCompletion(BaseModel):
    status: str = Field(description="OAuth completion status")
    message: str = Field(description="Completion message")
    accounts: Optional[List[AccountInfo]] = Field(description="Accounts after OAuth")


# For the final result
class TransactionFetchResult(BaseModel):
    status: str = Field(description="Overall status")
    accounts_fetched: int = Field(description="Number of accounts processed")
    transactions_fetched: int = Field(description="Number of transactions fetched")
    file_path: str = Field(description="Path to saved transactions file")
    summary: str = Field(description="Summary of the operation")
