from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Contact базова модель
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    # email: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None # необов"язкове поле


# Для створення нового контакту
class ContactCreate(ContactBase):
    first_name: str
    last_name: str
    # email: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None

    # @validator('first_name', 'last_name')
    # def name_must_not_be_empty(cls, v):
    #     if not v:
    #         raise ValueError('Name fields must not be empty')
    #     return v

    # @validator('phone')
    # def phone_must_be_valid(cls, v):
    #     if not v.isdigit():
    #         raise ValueError('Phone number must contain only digits')
    #     return v


# Для відображення даних контакту
class ResponseContact(ContactBase):
    id: int

    class Config:
        orm_mode = True


# Для оновлення контакту
class ContactUpdate(BaseModel): # для оновлення контакту.
    first_name: Optional[str] # всі поля optional - щоб можна було оновити вибіркові поля
    last_name: Optional[str]
    # email: Optional[str]
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
    # email: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    # email: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    # email: str
    email: EmailStr
    password: str