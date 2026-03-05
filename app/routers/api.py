from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import verify_token

router = APIRouter(prefix="/api", tags=["API"])

security = HTTPBearer()


# PROTECTED PROFILE
@router.get("/profile")
def get_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail={"error": "token_expired"})

    return {
        "id": 1,
        "username": payload["sub"],
        "email": payload["sub"],
        "roles": payload["roles"]
    }


# VERIFY TOKEN
@router.get("/verify-token")
def verify_access_token(token: str):

    payload = verify_token(token)

    if payload is None:
        return {
            "valid": False,
            "reason": "Token expired or invalid"
        }

    return {
        "valid": True,
        "claims": payload
    }