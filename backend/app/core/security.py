from fastapi import Header, HTTPException
from typing import Optional

# Token
VALID_TOKEN = "TEST_BEARER_TOKEN_2025"

def get_current_user(authorization: Optional[str] = Header(None)):
    """Valida el token Bearer en el encabezado Authorization."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, 
            detail="Token de autorización faltante o inválido. Formato: Bearer [token]"
        )
        
    token = authorization.split(" ")[1]
    