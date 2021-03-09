from fastapi.security.api_key import  APIKeyHeader, APIKey
from fastapi import HTTPException,Security
import os

API_KEY_NAME = "api_key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):

    if api_key == os.environ.get("API_CRUD_KEY"):
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )