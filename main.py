from portia import (
    Portia,
    McpToolRegistry,
    Config,
    InMemoryToolRegistry,
    DefaultToolRegistry,
)
from clarification_tool import ClarificationTool
from aml_financial_data_agent import AMLFinancialDataAgent
from aml_compliance_agent import AMLComplianceCheckAgent
from aml_suspicious_activity_report_agent import AMLSuspiciousActivityReportAgent

config = Config.from_default()

tools = (
    McpToolRegistry.from_stdio_connection(
        server_name="openbanking-agent",
        command="uv",
        args=["run", "openbanking_mcp/openbanking_mcp_server.py"],
    )
    + InMemoryToolRegistry([ClarificationTool()])
    + DefaultToolRegistry(config=config)
)

portia = Portia(config=config, tools=tools)

# for tool in tools.get_tools():
#     print(tool)

# Agent-1: Using the open banking MCP, it fetches the accounts and associated transactions
# and formats them into a JSON object. The output is saved in formatted_transactions.json.
openbanking_agent = AMLFinancialDataAgent(portia)
openbanking_agent.get_transactions_using_planBuilderV2()
openbanking_agent.format_transactions()

# Agent-2: Using the Anti-Money Laundering compliance check agent, it checks the transactions for AML.
# The result is saved in the aml_list.json file.
compliance_check_agent = AMLComplianceCheckAgent(portia)
compliance_check_agent.run_aml_check()

# Agent-3: Using the AML suspicious activity report agent, it generates a SAR report.
# The result is saved in the sar_report.txt file.
aml_suspicious_activity_report_agent = AMLSuspiciousActivityReportAgent(portia)
aml_suspicious_activity_report_agent.run_aml_suspicious_activity_report()
aml_suspicious_activity_report_agent.send_email_with_sar_report()
