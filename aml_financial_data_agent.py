from portia import Portia, PlanRunState, CustomClarification

from portia import PlanBuilderV2
from portia import StepOutput
from pydantic_base_models import (
    AccountsResponse,
    TransactionList,
    TransactionFetchResult,
)


class AMLFinancialDataAgent:
    """
    This agent is responsible for fetching transactions using the open banking MCP running locally.
    """

    def __init__(self, portia: Portia):
        self.portia = portia

    def get_transactions_using_planBuilderV2(self):
        plan = (
            PlanBuilderV2("Fetch transactions from Open Banking with OAuth flow")
            .invoke_tool_step(
                step_name="fetch_accounts",
                tool="mcp:openbanking-agent:fetch_accounts_tool",
                args={"kwargs": ""},
                output_schema=AccountsResponse,
            )
            .invoke_tool_step(
                step_name="request_oauth_code",
                tool="clarification",
                args={
                    "user_input": StepOutput(0),
                    "auth_code": "",
                },
            )
            .invoke_tool_step(
                step_name="complete_oauth",
                tool="mcp:openbanking-agent:complete_authorization_tool",
                args={"authorization_code": StepOutput("request_oauth_code")},
            )
            .llm_step(
                task="Extract the account UID from the OAuth completion result. Look for the 'uid' field in the accounts array. Return only the UID string, nothing else.",
                inputs=[StepOutput(2)],
            )
            .invoke_tool_step(
                step_name="fetch_transactions",
                tool="mcp:openbanking-agent:fetch_transactions_tool",
                args={"account_uid": StepOutput(3)},
                output_schema=TransactionList,
            )
            .invoke_tool_step(
                step_name="save_transactions",
                tool="file_writer_tool",
                args={
                    "filename": "transactions.txt",
                    "content": StepOutput("fetch_transactions"),
                },
            )
            .final_output(output_schema=TransactionFetchResult, summarize=True)
            .build()
        )

        plan_run = self.portia.run_plan(plan)
        while plan_run.state == PlanRunState.NEED_CLARIFICATION:
            clarifications = plan_run.get_outstanding_clarifications()
            for clarification in clarifications:
                if isinstance(clarification, CustomClarification):
                    print(f"\n{clarification.user_guidance}")
                    auth_code = input("📌Please provide your auth_code: ")
                    arg_map = {"auth_code": auth_code}
                    plan_run = self.portia.resolve_clarification(
                        clarification, arg_map, plan_run
                    )
            plan_run = self.portia.resume(plan_run)

    def format_transactions(self):
        format_transactions_task = """
        You are given a raw string containing messy transaction data in the file called transactions.txt.
        Read the file and your task is to **extract, clean, and reformat** this into **strict, valid JSON** that is easy to parse programmatically.

        **Instructions:**

        1. Ignore any irrelevant metadata, logs, or text like "Final output-", "value=", "summary=", or extra quotes and escape characters.
        2. Parse the transaction list accurately.
        3. For each transaction, include these fields:
        - entry_reference
        - booking_date
        - value_date
        - transaction_type (e.g., Debit, Credit)
        - amount:
            - currency
            - value
        - creditor:
            - name
            - address (or null if missing)
        - debtor (or null if missing)
        - description (if present in `remittance_information`)
        4. Ensure:
        - Strict JSON format
        - Arrays and objects are properly closed
        - No comments, no trailing commas
        - Use `null` where values are missing
        5. Write the formatted transactions to a file called formatted_transactions.json.
        **Output format:**
        ```json
        {
        "transactions": [
            {
            "entry_reference": "tx1003",
            "booking_date": "2025-08-23",
            "value_date": "2025-08-23",
            "transaction_type": "Debit",
            "amount": {
                "currency": "EUR",
                "value": 9800.00
            },
            "creditor": {
                "name": "Ahmed Khan (UAE)",
                "address": null
            },
            "debtor": null,
            "description": "High-value international transfer to high-risk jurisdiction"
            }
        ]
        }
        """
        self.portia.run(format_transactions_task)
        print("Done! The transactions have been formatted.")
