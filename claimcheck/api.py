"""Thin FastAPI layer. Routes validate, delegate to agent/runner/db, and map
errors to sanitized {"error": {"type", "message"}} bodies."""
from __future__ import annotations

import uuid
from functools import lru_cache
from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from . import config
from .agent import run_agent
from .db import Database
from .facts_tool import FactStore
from .providers import ProviderFactory, live_provider_factory
from .runner import run_evaluation
from .schemas import AgentInput, ClassifyRequest, EvaluationRunRequest

app = FastAPI(title="claimcheck", version="1.0")

HTTP_FOR_ERROR = {"unknown_primary_brand": 404, "provider_timeout": 504}


def error_body(status: int, etype: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"type": etype, "message": message}})


@app.exception_handler(RequestValidationError)
async def _validation_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    # Sanitized: report field locations and messages, never echo input values.
    fields = [{"loc": [str(p) for p in e.get("loc", ())], "msg": e.get("msg")} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"error": {"type": "validation_error",
                                                            "message": "request validation failed",
                                                            "fields": fields}})


# ---------------------------------------------------------------- dependencies (overridable in tests)
@lru_cache
def get_store() -> FactStore:
    return FactStore()


def get_settings() -> config.Settings:
    return config.load_settings()


def get_provider_factory() -> ProviderFactory:
    return live_provider_factory(config.load_settings())


@lru_cache
def _database() -> Database:
    db = Database(config.database_url() or "")
    db.init_schema()
    return db


def get_db() -> Database:
    return _database()


# ---------------------------------------------------------------- routes
@app.post("/classify")
def classify(req: ClassifyRequest, store: FactStore = Depends(get_store),
             settings: config.Settings = Depends(get_settings),
             provider_factory: ProviderFactory = Depends(get_provider_factory)) -> Any:
    if not store.has_brand(req.brand_id):
        return error_body(404, "unknown_primary_brand", "brand_id is not in the catalogue")
    inp = AgentInput(answer_id=req.answer_id, brand_id=req.brand_id, question=req.question, ai_answer=req.ai_answer)
    result = run_agent(inp, req.agent_version, provider_factory(req.answer_id), store, settings)
    if result.status != "ok":
        status = HTTP_FOR_ERROR.get(result.error_type or "", 502)
        return error_body(status, result.error_type or "agent_error", result.error_message or "agent failed")
    return {"answer_id": result.output.answer_id, "agent_version": req.agent_version,
            "claims": [c.model_dump() for c in result.output.claims]}


@app.post("/evaluation-runs", status_code=201)
def create_evaluation_run(req: EvaluationRunRequest, store: FactStore = Depends(get_store),
                          settings: config.Settings = Depends(get_settings),
                          provider_factory: ProviderFactory = Depends(get_provider_factory),
                          db: Database = Depends(get_db)) -> Any:
    summary = run_evaluation(req.agent_version, req.split, provider_factory, provider_factory.name,
                             provider_factory.model, db, settings, store=store)
    return {"run_id": summary["run_id"], "status": summary["status"], "counts": summary["counts"],
            "metrics": summary["metrics"]}


@app.get("/evaluation-runs/{run_id}")
def get_evaluation_run(run_id: uuid.UUID, db: Database = Depends(get_db)) -> Any:
    run = db.get_run(run_id)
    if run is None:
        return error_body(404, "run_not_found", "no evaluation run with this id")
    if run["split"] == "check":
        for a in run["answers"]:
            for c in a["claims"]:
                for k in ("gold_match", "gold_claim_id", "expected_label", "label_correct"):
                    c[k] = None
    return run
