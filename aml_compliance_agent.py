from portia import Portia


class AMLComplianceCheckAgent:
    def __init__(self, portia: Portia):
        self.portia = portia

    def run_aml_check(self):
        """
        This method is responsible for running the AML compliance check.
        """
        compliance_check_task = """
        1. Read transactions from formatted_transactions.json.
        2. Run AML analysis on transactions_data and return a STRICT JSON object:
        {
            "flagged_transactions": [ { ...original transaction..., "risk_score": "...", "reasons": ["..."] } ],
            "clean_transactions":   [ { ... } ],
            "summary": "..."
        }
        If none flagged, return an empty array for flagged_transactions.
        3. IF len(flagged_transactions) > 0:
            Write ONLY flagged_transactions (pretty-printed JSON) to aml_list.txt
        4. ELSE:
            Return clean_transactions.
        5. Write the JSON from step 2 in a file called aml_list.txt
        """
        plan_run = self.portia.run(compliance_check_task)
        print(plan_run.outputs.final_output)
        print("Done! The AML compliance check has been run.")
