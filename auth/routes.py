from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.session import get_db
from db.models import User
from auth.utils import hash_password, verify_password, create_jwt

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(400, "Email already registered")

    new_user = User(email=email, password_hash=hash_password(password))
    db.add(new_user)
    await db.commit()

    return {"message": "Signup successful"}


@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")

    token = create_jwt({"user_id": user.id})
    return {"access_token": token}
