# kovrex-fastapi-agent-template

Minimal FastAPI template for a Kovrex operator agent.

## What this includes
- FastAPI app with a single POST endpoint (`/v1/hello`)
- Stable request/response models (Pydantic)
- Structured refusal responses
- Optional shared-secret auth via `X-Agent-Secret`
- `/health` endpoint
- Dockerfile for deployment

## Quickstart

### 1) Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Test:

```bash
curl -s -X POST http://localhost:8000/v1/hello \
  -H 'Content-Type: application/json' \
  -d '{"name":"Sean"}'
```

### 2) Docker

```bash
docker build -t hello-agent .
docker run -p 8000:8000 hello-agent
```

## Registering on Kovrex

In the Kovrex Operator dashboard:
- Set your endpoint base URL (where you deploy this)
- Route: `/v1/hello`
- Provide input/output schemas (see `kovrex/` folder)
- If you set `AGENT_SECRET_KEY`, paste it into the agent registration as the secret

## License
MIT
