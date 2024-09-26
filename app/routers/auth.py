# Реєстрація користувача: створюю новий роутер для реєстрації і авторизації
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from app.schemas import UserCreate, UserRead, UserLogin
from app.repository.contact_model import User
from app.database import get_db
from passlib.hash import bcrypt

router = APIRouter(prefix="/auth", tags=["Authentication"])

# реєстрація користувача
@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # чек - чи немає часом користувача із таким же мейлом
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")

    hashed_password = bcrypt.hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# логін користувача та генерація токенів
@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not user.verify_password(user_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
