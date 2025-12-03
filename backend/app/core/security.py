from fastapi import Header, HTTPException
from typing import Optional

# Token
VALID_TOKEN = "TEST_BEARER_TOKEN_2025"

def get_current_user(authorization: Optional[str] = Header(None)):
    """Valida el token Bearer en el encabezado Authorization."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    token = authorization.split(" ")[1]

    if token != VALID_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

    return token

    