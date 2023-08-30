from app.api.modules.tokens.access_token import JWTAuthentication


jwt_auth = JWTAuthentication(
    secret_key="your-secret-key",
    algorithm="HS256",
    access_token_expire_minutes=30
)
