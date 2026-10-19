from typing import Any
from fastapi import FastAPI, HTTPException
from app.logic import processar_solicitacao

app = FastAPI(title="RPA de Triagem de Compras", version="1.0.0")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "servico": "rpa-triagem-compras"}

@app.post("/processar")
def processar(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        return processar_solicitacao(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
