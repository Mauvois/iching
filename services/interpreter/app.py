import logging
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
from pydantic import BaseModel


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InterpretationRequest(BaseModel):
    question: str
    iching_response: str


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")
    return OpenAI(api_key=api_key)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/interpret")
async def interpret(request: InterpretationRequest):
    if not request.question or not request.iching_response:
        raise HTTPException(status_code=400, detail="Both question and I Ching response are required.")

    prompt = (
        f"L'utilisateur a demande: {request.question}\n"
        f"I Ching a repondu: {request.iching_response}\n"
        "Fournis une interpretation en 2 courts paragraphes"
    )

    try:
        client = get_openai_client()
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        interpretation = completion.choices[0].message.content.strip()
        return {"interpretation": interpretation}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error during OpenAI API call")
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
