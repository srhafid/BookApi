import datetime
from functools import wraps
import jwt
from fastapi import Header, HTTPException, Depends, FastAPI


class JWTAuthentication:
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_token(self, data: dict) -> str:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=self.expire_minutes
        )
        data.update({"exp": expire})
        token = jwt.encode(data, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")


auth = JWTAuthentication(secret_key="secret", algorithm="HS256", expire_minutes=30)


def get_current_user(authorization: str = Header(...)):
    token = authorization.split()[1]
    return auth.verify_token(token)


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, current_user: dict = Depends(get_current_user), **kwargs):
        return await func(*args, current_user=current_user, **kwargs)

    return wrapper
