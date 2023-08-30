"""
JWTAuthentication: Helper class for JWT token management.

This class provides methods to create and verify JWT tokens.
"""

import datetime
from functools import wraps
import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, DecodeError
from fastapi import HTTPException, Header


class JWTAuthentication:
    """
    JWTAuthentication class provides methods to create and verify JWT tokens.

    Args:
        secret_key (str): Secret key used for JWT encoding and decoding.
        algorithm (str): Algorithm used for JWT encoding and decoding.
        access_token_expire_minutes (int): Expiration time for access tokens in minutes.

    Attributes:
        secret_key (str): Secret key used for JWT encoding and decoding.
        algorithm (str): Algorithm used for JWT encoding and decoding.
        access_token_expire_minutes (int): Expiration time for access tokens in minutes.
        oauth2_scheme (OAuth2PasswordBearer): OAuth2PasswordBearer instance for token URL.
    """

    def __init__(
        self, secret_key: str, algorithm: str, access_token_expire_minutes: int
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def create_access_token(self, data: dict) -> str:
        """
        Create a JWT access token with the provided data.

        Args:
            data (dict): Data to include in the token payload.

        Returns:
            str: Encoded JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=self.access_token_expire_minutes
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> dict:
        """
        Verify a JWT token and return its payload.

        Args:
            token (str): JWT token to verify.

        Returns:
            dict: Decoded payload of the verified JWT token.

        Raises:
            HTTPException: If token is expired or invalid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def token_required(self, func):
        """
        Decorator to require a valid JWT token for a function.

        Args:
            func (callable): The function to be decorated.

        Returns:
            callable: Decorated function with JWT token verification.
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                authorization_header = Header(None)
                token = authorization_header()

                if token is None:
                    raise HTTPException(status_code=401, detail="Token not provided")

                payload = jwt.decode(
                    token, self.secret_key, algorithms=[self.algorithm]
                )
                kwargs["current_user"] = payload
                return await func(*args, **kwargs)
            except ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except DecodeError:
                raise HTTPException(status_code=401, detail="Invalid token")

        return wrapper
