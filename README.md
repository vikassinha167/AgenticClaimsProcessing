# AgenticClaimsProcessing

## Architecture Overview

AgenticClaimsProcessing is a production-grade Azure AI Foundry-centered healthcare claims processing system. It implements an AutoGen-style multi-agent workflow with the following components:

- Planner Agent: orchestrates the workflow and selects the end-to-end processing path.
- Extraction Agent: ingests claims as structured JSON or documents and extracts normalized claim data via Azure Document Intelligence.
- Coding Agent: performs ICD/CPT mapping using Azure OpenAI reasoning and prompt templates.
- Validation Agent: evaluates claim compliance against policy rules served by a local MCP server.
- Fraud Detection Agent: combines Azure AI Search RAG, external fraud scoring API, and hybrid reasoning.
- Decision Agent: makes the final outcome (Approve, Reject, Flag for Review).
- Critic Agent: validates groundedness, relevance, and safety and ensures Responsible AI guardrails.
- Evaluation Pipeline: computes groundedness, relevance, safety, and fraud confidence metrics and stores results in Azure AI Foundry.

## Azure Services Mapping

| Capability | Azure Service | Implementation | Notes |
|---|---|---|---|
| LLM | Azure OpenAI | `app.tools.openai_client.py` | Uses GPT-4o deployment and prompt templates.
| Document Extraction | Azure Document Intelligence | `app.tools.document_intelligence.py` | Extracts structured claim fields from document assets.
| RAG / Search | Azure AI Search | `app.tools.ai_search.py` | Retrieves fraud pattern evidence for risk assessment.
| Responsible AI | Azure Content Safety | `app.tools.content_safety.py` | Enforces content guardrails and safety checks.
| Control Plane | Azure AI Foundry | `app.tools.foundry_sdk.py` | Registers agents and logs trace/evaluation artifacts.
| Policy Rules | MCP Server | `app/mcp/server.py` | Serves policy definitions as a centralized rules endpoint.

## GitHub Repo Structure

- `app/` - Core application package.
  - `agents/` - Multi-agent orchestrator and domain agents.
  - `tools/` - Azure integrations, policies, and external API connectors.
  - `mcp/` - MCP-style policy server and schemas.
  - `evaluations/` - Evaluation metrics and Foundry pipeline.
  - `data/sample/` - Representative healthcare claim payloads.
- `scripts/` - Local runner, evaluation runner, Foundry registration, and MCP server bootstrap.
- `.env.example` - Required environment variables for production deployment.
- `requirements.txt` - Python dependency manifest.

## Step-by-Step Azure Setup

1. Create Azure AI Foundry project:
   - Provision an Azure AI Foundry workspace and project.
   - Generate API credentials and the project ID.
   - Copy the Foundry endpoint and API key into `.env`.

2. Deploy Azure OpenAI model:
   - Create an Azure OpenAI resource.
   - Deploy `gpt-4o` or equivalent.
   - Set `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, and `AZURE_OPENAI_DEPLOYMENT`.

3. Configure Document Intelligence:
   - Provision Azure Document Intelligence or Form Recognizer.
   - Create a key and endpoint.
   - Set `AZURE_FORM_RECOGNIZER_ENDPOINT` and `AZURE_FORM_RECOGNIZER_KEY`.

4. Configure Azure AI Search:
   - Create an Azure Cognitive Search resource.
   - Create an index for fraud patterns, e.g. `healthcare-fraud-index`.
   - Set `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY`, and `AZURE_SEARCH_INDEX`.

5. Configure Responsible AI guardrails:
   - Provision Azure Content Safety if available.
   - Set `AZURE_CONTENT_SAFETY_ENDPOINT` and `AZURE_CONTENT_SAFETY_KEY`.

6. External Fraud Scoring API:
   - Configure a real or mock API endpoint with a bearer key.
   - Set `FRAUD_API_URL` and `FRAUD_API_KEY`.

7. Local MCP server:
   - Start the MCP policy server using `scripts/run_mcp.py`.
   - Ensure `MCP_HOST` and `MCP_PORT` are set before running.

## Agent Registration in Foundry

1. Configure your `.env`.
2. Run:
```bash
python scripts/deploy_foundry_agents.py
```
3. This registers each named agent into the Foundry project and makes the agents visible via the project UI.

## Evaluation Setup

1. The evaluation pipeline is implemented in `app/evaluations/evaluator.py`.
2. Evaluation metrics include:
   - groundedness
   - relevance
   - safety
   - fraud_detection_confidence
3. Results are stored in Foundry using `FoundryClient.store_evaluation`.
4. Run evaluations locally with:
```bash
python scripts/eval_run.py
```

## Guardrails Implementation

- Content Safety checks are enforced by `app.tools.content_safety.ContentSafetyClient`.
- Policy and claims rules are centralized in the MCP server under `app/mcp/`.
- The Critic Agent validates outputs for groundedness and bias.

## Run Instructions

1. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

2. Create `.env` from `.env.example` and populate secrets.

3. Start the MCP server:
```bash
python scripts/run_mcp.py
```

4. Optionally register agents in Foundry:
```bash
python scripts/deploy_foundry_agents.py
```

5. Run a local claim processing orchestration:
```bash
python scripts/run_local.py
```

6. Run the evaluation pipeline:
```bash
python scripts/eval_run.py
```

## Sample Data

- `app/data/sample/claim_sample.json` contains a representative healthcare claim with two service lines.

## Notes

- The system is designed for enterprise Azure Foundry deployments, with centralized policy rules and audit trails.
- All secrets are loaded from `.env`; no values are hardcoded.
- The solution is modular and can be extended to support high-scale ingestion, custom workflows, and additional Foundry observability.
