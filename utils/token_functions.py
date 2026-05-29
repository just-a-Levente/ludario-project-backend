from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Cookie, HTTPException, Depends, status

SECRET_KEY = "super-duper-top-secret-key-dont-look"
ALGORITHM = "HS256"

ACCESS_TOKEN_LIVE_INTERVAL = timedelta(minutes=15)
REFRESH_TOKEN_LIVE_INTERVAL = timedelta(hours=24)

def create_access_token(user_email: str, roles: list[str], permissions: list[str]) -> str:
    return jwt.encode({
        "sub": user_email,
        "roles": roles,
        "permissions": permissions,
        "exp": datetime.now(timezone.utc) + ACCESS_TOKEN_LIVE_INTERVAL,
        "type": "access"
    }, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_email: str) -> str:
    return jwt.encode({
        "sub": user_email,
        "exp": datetime.now(timezone.utc) + REFRESH_TOKEN_LIVE_INTERVAL,
        "type": "refresh"
    }, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401)
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def require_permission(permission: str):
    def dependency(user = Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return dependency