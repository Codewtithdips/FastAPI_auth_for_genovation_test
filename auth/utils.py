from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT creation
def create_jwt(data: dict, expires_in: int = 3600) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(seconds=expires_in)

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm="HS256"
    )

    return token
