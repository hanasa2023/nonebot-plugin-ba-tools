from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from ...config import ConfigManager

security = HTTPBearer()


def verify_token(cred: HTTPAuthorizationCredentials = Depends(security)):
    try:
        jwt.decode(
            cred.credentials,
            ConfigManager.get().webui.api_access_token,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
