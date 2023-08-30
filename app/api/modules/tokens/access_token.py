import datetime
from functools import wraps
import jwt
from fastapi import Header, HTTPException, Depends, FastAPI

class JWTAuthentication:
    """
    Helper class for JWT token authentication.
    """
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        """
        Initialize JWTAuthentication instance.

        Args:
            secret_key (str): Secret key for JWT encoding and decoding.
            algorithm (str): Algorithm used for JWT encoding and decoding.
            expire_minutes (int): Token expiration time in minutes.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_token(self, data: dict) -> str:
        """
        Create a JWT token with the provided data.

        Args:
            data (dict): Data to be encoded in the JWT token.

        Returns:
            str: Encoded JWT token.
        """
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=self.expire_minutes
        )
        data.update({"exp": expire})
        token = jwt.encode(data, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> dict:
        """
        Verify and decode a JWT token.

        Args:
            token (str): JWT token to be verified.

        Returns:
            dict: Decoded payload of the JWT token.

        Raises:
            HTTPException: If token is expired or invalid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")

# Initialize JWTAuthentication instance
auth = JWTAuthentication(secret_key="secret", algorithm="HS256", expire_minutes=30)

def get_current_user(authorization: str = Header(...)):
    """
    Get the current user from the JWT token.

    Args:
        authorization (str): Authorization header containing the JWT token.

    Returns:
        dict: Decoded payload of the JWT token.
    """
    token = authorization.split()[1]
    return auth.verify_token(token)

def auth_required(func):
    """
    Decorator to require authentication for a route.

    Args:
        func (callable): The route function to be decorated.

    Returns:
        callable: Decorated route function.
    """
    @wraps(func)
    async def wrapper(*args, current_user: dict = Depends(get_current_user), **kwargs):
        return await func(*args, current_user=current_user, **kwargs)

    return wrapper
