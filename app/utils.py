import jwt
from app.config import jwt_settings
from datetime import datetime, timedelta


def generate_access_token(
        data: dict,
        expiry: timedelta = timedelta(days=1)
) -> str | None:
    try:
        return jwt.encode(
            payload={
                **data,
                "exp": datetime.now() + timedelta(days=1)
            },
            algorithm=jwt_settings.JWT_ALGORITHM,
            key=jwt_settings.JWT_SECRET_KEY
        )
    except jwt.PyJWTError:
        return None


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=jwt_settings.JWT_SECRET_KEY,
            algorithms=[jwt_settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        return None
