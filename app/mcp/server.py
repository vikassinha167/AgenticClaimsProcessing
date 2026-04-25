from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.mcp.policies import DEFAULT_POLICY
from app.mcp.schemas import PolicyBundle

app = FastAPI(title="MCP Policy Server", version="1.0.0")


@app.get("/policies", response_model=PolicyBundle)
def get_policies() -> PolicyBundle:
    return DEFAULT_POLICY


@app.get("/constraints")
def get_constraints() -> JSONResponse:
    constraints = {
        "allowed_procedures": DEFAULT_POLICY.allowed_procedures,
        "max_line_item_amount": DEFAULT_POLICY.max_line_item_amount,
        "exceptions": DEFAULT_POLICY.exceptions,
    }
    return JSONResponse(content=constraints)


@app.get("/allowed-procedures")
def get_allowed_procedures() -> JSONResponse:
    return JSONResponse(content={"allowed_procedures": DEFAULT_POLICY.allowed_procedures})


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})
