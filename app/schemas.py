from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date


# Contact базова модель
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None # необов"язкове поле


# Для створення нового контакту
class ContactCreate(ContactBase):
    pass # не потрібно знову всі поля прописувати, бо вони вже спадкуються від ContactBase
    # first_name: str
    # last_name: str
    # email: EmailStr
    # phone: str
    # birthday: date
    # additional_info: Optional[str] = None


# Для відображення даних контакту
class ResponseContact(ContactBase):
    id: int
    owner_id: int  # Додаємо поле owner_id для відображення ID власника

    class Config:
        orm_mode = True


# Для оновлення контакту
class ContactUpdate(BaseModel): # для оновлення контакту.
    first_name: Optional[str] # всі поля optional - щоб можна було оновити вибіркові поля
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    birthday: Optional[date]
    additional_info: Optional[str]
    
    class Config:
        orm_mode = True


# Для відображення контактів із додатковою інформацією про власника
class ContactRead(ResponseContact):
    owner_id: int

    class Config:
        orm_mode = True


# Додаю схеми для реєстрації і авторизації користувачів
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Схема для відображення користувача
class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool  # Додаємо поле is_active, оскільки воно є у моделі User

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Схема для відображення користувача з прив'язаними контактами
class UserWithContacts(UserRead):
    contacts: List[ResponseContact] = []  # Додаємо список контактів користувача

    class Config:
        orm_mode = True