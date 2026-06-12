import os
from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

security = HTTPBearer(auto_error=False)


@dataclass
class AuthUser:
    id: UUID
    email: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> AuthUser:
    """Validate Supabase JWT. In dev without secret, accepts X-Dev-User header pattern."""
    jwt_secret = os.environ.get("SUPABASE_JWT_SECRET", "")

    if not credentials:
        if os.environ.get("ENVIRONMENT") == "development":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing Authorization header",
            )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = credentials.credentials
    if not jwt_secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="SUPABASE_JWT_SECRET not configured",
        )

    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"], audience="authenticated")
        sub = payload.get("sub")
        email = payload.get("email", "")
        if not sub:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return AuthUser(id=UUID(sub), email=email)
    except (JWTError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
