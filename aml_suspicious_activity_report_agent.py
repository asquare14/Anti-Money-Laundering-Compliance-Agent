from portia import Portia
from openbanking_mcp.openbanking_config import EMAIL_ADDRESS


class AMLSuspiciousActivityReportAgent:
    def __init__(self, portia: Portia):
        self.portia = portia

    def run_aml_suspicious_activity_report(self):
        """
        This method is responsible for generating the AML suspicious activity report.
        """
        sar_from_aml_list_task = """
        Goal: Generate a SAR report from the AML list.
        Steps:
        1. Read aml_list.txt
        2. Summarize suspicious activity:
        - Mention who, what, when, where, why.
        - Include transaction refs, dates, amounts, currencies, and counterparties.
        3. Add sections:
        - Reason for Suspicion (2–3 sentences)
        - Risk Indicators (bullets)
        - Flagged Transactions (one line per tx: ref, date, amount, receiver, reason)
        - Overall Risk (High/Medium/Low)
        - Recommendations (File SAR, EDD, monitoring)
        4. Use concise, factual, professional tone.
        5. Output plain text only, write that to a file called sar_report.txt.
        """
        self.portia.run(sar_from_aml_list_task)

    def send_email_with_sar_report(self):
        """
        This method is responsible for sending the SAR report to the email.
        """
        send_email_task = f"""
        Goal: Send the SAR report sar_report.txt to the email {EMAIL_ADDRESS}
        """
        self.portia.run(send_email_task)
