from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None # необов"язкове поле

class ResponseContact(ContactBase):
    id: int

    class Config:
        orm_mode = True


class ContactUpdate(BaseModel): # для оновлення контакту.
    first_name: Optional[str] # всі поля optional - щоб можна було оновити вибіркові поля
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    birthday: Optional[date]
    additional_info: Optional[str]
    
    class Config:
        orm_mode = True

# Додаю схеми для реєстрації і авторизації
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str