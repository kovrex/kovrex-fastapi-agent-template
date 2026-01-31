import hmac
import os

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.models import HelloRequest, HelloResponse, RefusalCode, RefusalResponse

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
AGENT_SECRET_KEY = os.getenv("AGENT_SECRET_KEY", "")  # optional

app = FastAPI(title="Hello Agent", version=APP_VERSION)


def verify_agent_secret(request: Request) -> JSONResponse | None:
    """Optional auth: verify X-Agent-Secret header if AGENT_SECRET_KEY is configured."""
    if not AGENT_SECRET_KEY:
        return None

    provided = request.headers.get("X-Agent-Secret")
    if not provided:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=RefusalResponse(
                refused=True,
                refusal_code=RefusalCode.UNAUTHORIZED,
                refusal_reason="Missing X-Agent-Secret header",
            ).model_dump(),
        )

    if not hmac.compare_digest(provided, AGENT_SECRET_KEY):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=RefusalResponse(
                refused=True,
                refusal_code=RefusalCode.UNAUTHORIZED,
                refusal_reason="Invalid X-Agent-Secret header",
            ).model_dump(),
        )

    return None


@app.get("/health")
async def health():
    return {"status": "ok", "version": APP_VERSION}


@app.post("/v1/hello", response_model=HelloResponse | RefusalResponse)
async def hello(request: Request, payload: HelloRequest):
    secret_check = verify_agent_secret(request)
    if secret_check is not None:
        return secret_check

    # Example scope boundary (optional): refuse certain names
    if payload.name.strip().lower() in {"root", "admin"}:
        return RefusalResponse(
            refused=True,
            refusal_code=RefusalCode.OUT_OF_SCOPE,
            refusal_reason="This agent will not greet privileged identities",
        )

    return HelloResponse(message=f"hello {payload.name}", version=APP_VERSION)
