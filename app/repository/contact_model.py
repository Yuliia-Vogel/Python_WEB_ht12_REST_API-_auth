from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt

from ..database import Base, engine

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)


class User(Base): # додаємо клас User на основі раніше створеного класу Base 
    __tablename__ = 'users' # назва таблиці з користувачами (sqlite)
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False) # унікальна пошта
    hashed_password = Column(String, nullable=False) # хешований пароль (який не зберігається у відкритому вигляді)
    is_active = Column(Boolean, default=True) # доступ до бази за замовчуванням дозволений
    
    contacts = relationship("Contact", back_populates="owner")

    def verify_password(self, password: str) -> bool: # для перевірки введеного пароля
        return bcrypt.verify(password, self.hashed_password) # за допомогою bcrypt при реєстрації
    # При логіні порівнюється хешований пароль із введеним.