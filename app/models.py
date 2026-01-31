from enum import Enum
from pydantic import BaseModel, Field


class RefusalCode(str, Enum):
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    UNAUTHORIZED = "UNAUTHORIZED"


class HelloRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)


class HelloResponse(BaseModel):
    message: str
    version: str = "0.1.0"


class RefusalResponse(BaseModel):
    refused: bool = True
    refusal_code: RefusalCode
    refusal_reason: str
