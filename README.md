# Anti Money Laundering Agent


### Glossary

- **AML (Anti-Money Laundering)**: A set of laws, regulations, and procedures designed to prevent criminals from disguising illegally obtained funds as legitimate income. AML processes include transaction monitoring, customer due diligence (CDD), and reporting suspicious activity.

- **Open Banking**: A financial services framework that allows banks to securely share customer data (with consent) through APIs. It enables third-party providers to offer innovative financial services, such as budgeting tools, payment initiation, and account aggregation.

- **EnableBanking**: A platform that provides a unified API for accessing financial data and initiating payments across multiple banks through open banking protocols. Often used by fintechs and compliance systems to streamline connectivity with multiple banks.

- **SAR (Suspicious Activity Report)**: A document filed by financial institutions to report suspicious transactions that may indicate money laundering, terrorist financing, or other criminal activities.

- **MCP (Model Context Protocol)**: A standardized way for applications to provide context and tools to Large Language Models, enabling AI agents to interact with external systems and data sources.

### Overview

Detecting and preventing money laundering is a mission-critical requirement for financial institutions and fintech platforms, but the process is often slow, manual, and error-prone.

This project bridges that gap by combining real-time Open Banking data with an intelligent multi-agent system, built using the Model Context Protocol (MCP).


Demo - https://www.youtube.com/watch?v=kgmcXldp_-M

**Instant insights**: Real-time transaction retrieval from banks via the Enable Banking API.

**Smarter compliance**: Automated rule-based and AI-assisted analysis flags suspicious activity like high-value transfers, crypto purchases, or transactions with high-risk jurisdictions.

**Actionable reports**: Generates ready-to-submit Suspicious Activity Reports (SARs) that comply with AML regulations like UK MLR 2017 and POCA 2002.

This makes the system scalable, plug-and-play, and adaptable for banks, payment processors, and AML compliance teams.

### Creativity and Originality

- **MCP-first architecture**: Created my own open banking MCP for the project. The project integrates MCP servers with AI agents, enabling tool registration and chaining.

- **Open Banking synergy**: Combines bank APIs with compliance automation, something rarely seen in hackathon demos.

- **Multi-agent design**: Transaction Retrieval Agent for secure data fetches, Compliance Agent for AML checks, powered by both deterministic rules and LLM reasoning, SAR Generator Agent for formatted, regulator-ready reports.

- **Future scalability**: Architecture is modular — ready to integrate more agents like periodic monitoring, graph analysis for money flow, or human-in-the-loop audit approvals.

### Learning and Growth

- Gained expertise in Open Banking and the Enable Banking API, including authentication, JWT signing, and secure session handling.

- Learned the MCP protocol and implemented my first evert MCP and integrated it with Portia SDK for smooth tool orchestration.

- Improved prompt engineering and multi-agent coordination for deterministic + LLM hybrid pipelines.

- Learned to debug real-world integration issues, including OAuth flows, sandbox inconsistencies, and MCP stdio communication.


## Tech stack:

- **Python** – core logic, rule-checker, JWT authentication

- **Enable Banking API** – Open Banking connectivity

- **MCP (Model Context Protocol)** – structured, interoperable server for agent tools

- **Portia AI SDK** – agent orchestration and chaining

- **LLMs** – SAR generation and advanced compliance reasoning

## 🏗️ Architecture

### Core Components
1. **Financial Data Agent**: AI agent that gets the banking transactions.
2. **Open Banking MCP Server**: — MCP service layering on a custom EnableBanking client to provide AI-accessible tools for financial data access and payments.
Tools: fetch_accounts, fetch_transactions, complete_authorization
3. **AML Analysis Engine**: AI agent that flags transactions as AML.
4. **SAR Report Generator**: AI agent that generates automated regulatory report creation.

### Data Flow

1. **Financial Agent asked to get transaction** – User or system triggers a fetch request for recent banking transactions.
2. **MCP Layer** – MCP server handles the API request to the connected bank via Open Banking APIs.
3. **OAuth Consent** – MCP initiates secure OAuth flow for account access.
4. **User Interaction** – User is prompted to authorize and paste the **access token** back into the system.
5. **Resume Process** – MCP validates the token and securely retrieves the requested transaction data.
6. **Transaction Formatting** – Normalize and clean transaction data into a consistent internal schema.
7. **Compliance Agent** – Analyze transactions for AML risks and generate flagged vs. clean transaction sets.
8. **SAR Generator Agent** – Convert flagged transactions into a structured SAR payload and human-readable narrative.
9. **Email Notification** – Automatically email the SAR report to compliance officers or a secure mailbox.

## How you can use it

### Prerequisites
- Python 3.8+
- Portia API key
- OpenAI API key
- Open Banking credentials (EnableBanking)
- Private key file from Enable Banking (.pem)

### Setup enable banking

1. Go to https://enablebanking.com/cp/applications and create an application.
2. Add http://127.0.0.1:8765/callback in allowed redirect uris.
3. Once your app is created, download a pem file and the app-id and keep it handy for running the application.
4. Add these to openbanking_config.py along with email that you want SAR report to go to.
5. Next go to https://enablebanking.com/cp/mock-aspsp
6. Create a mock account and mock transactions.
7. You can use chatgpt to generate mock shady transactions.

Note: I have for now committed my own .pem file and app id so that you can run the project out of box
as I didn't have time to integrate with a key management service. Ideally this should not be done and these will
be deactivated after the hackathon.

## Running locally
```bash
# Install dependencies
uv sync

# Start OAuth callback server in terminal 1
uv run oauth_callback_server.py

# Run MCP server in terminal 2
uv run mcp run openbanking_mcp/openbanking_mcp_server.py

# Execute main agent in terminal 3
uv run main.py
```

## 📁 Project Structure

```
anti-money-laundering-agent/
├── main.py                          # Main agent execution
├── oauth_callback_server.py         # OAuth authorization handler
├── openbanking-mcp/                 # Open Banking MCP server
│   ├── openbanking_mcp_server.py   # MCP server implementation
│   ├── openbanking_mcp_tool.py     # Open Banking API tools
│   └── openbanking_client.py       # EnableBanking client
├── aml_suspicious_activity_report_agent.py  # SAR generation logic
├── aml_financial_data_agent.py     # Gets transactions from open banking
├── aml_compliance_agent.py         # Checks for compliance
├── pydantic_base_models.py 
├── pyproject.toml                   # Project dependencies
└── README.md                        # This file
```

## 🔧 Configuration

### Environment Variables
```bash
PORTIA_API_KEY=your_portia_key
OPENAI_API_KEY=your_openai_key
```

## 📈 Future Enhancements

* **Real-Time Intelligence** – Instant detection and alerts for suspicious transactions, empowering teams to act the moment risk is identified.
* **Global Compliance Ready** – Seamlessly adapts to international regulations, from FCA and FinCEN to FATF frameworks, ensuring worry-free scalability.
* **Plug-and-Play Integration** – Easily connects to any financial platform, core banking system, or payment processor with minimal setup.
* **Next-Gen Dashboard** – A sleek, interactive interface delivering real-time analytics, risk scoring, and one-click SAR generation.