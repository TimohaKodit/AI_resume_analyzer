import os
from fastapi import APIRouter, HTTPException
from schemas import UserRegister
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select
from models import User
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

auth_router = APIRouter()


pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated = 'auto'
)



@auth_router.post('/auth/register')
async def reg(item: UserRegister, db: AsyncSession = Depends(get_db)):
    search = await db.execute(select(User).where(User.email == item.email))
    user = search.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail='Пользователь с таким email уже зарегистрирован')
    else:
        hash_pass = pwd_context.hash(item.password)
        new_user = User(
            email=item.email,
            hashed_password=hash_pass
        )
        db.add(new_user)
        await db.commit()
        return "Аккаунт успешно зарегистрирован"


@auth_router.post("/auth/login")
async def login_func(item: UserRegister, db: AsyncSession = Depends(get_db)):
    search = await db.execute(select(User).where(User.email == item.email))
    user = search.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь с таким EMAIL не найден")
    else:
        correct_pass = pwd_context.verify(item.password, user.hashed_password)
        if not correct_pass:
            raise HTTPException(status_code=404, detail='Пароль неверный')
        else:
            secret = os.getenv("SECRET_KEY")
            algo = 'HS256'
            payload = {
                "user": user.id,
                "email": item.email,
                "exp": datetime.utcnow() + timedelta(minutes=10)
            }

            token = jwt.encode(payload, secret, algorithm=algo)
    return token
