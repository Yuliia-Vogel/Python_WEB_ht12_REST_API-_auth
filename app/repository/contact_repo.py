from datetime import date, timedelta # для пошуку днів народження

from sqlalchemy.orm import Session
from .contact_model import Contact
from ..schemas import ContactBase


def get_one_contact(db: Session, contact_id: int): # отримати контакт за його id
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contacts(db: Session, first_name: str = None, last_name: str = None, email: str = None): # вивести список всіх контактів чи для пошуку за іменем, прізвищем чи ємейлом
    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()


def create_contact(db: Session, contact: ContactBase): # cстворення контакту
    new_contact = Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def delete_contact(db: Session, contact_id: int): # для видалення контакту
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()


def get_contact_by_id(db: Session, contact_id: int): # отримати контакт для оновлення даних
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contacts_with_upcoming_birthdays(db: Session): # для пошуку днів народж. у найбл. 7 днів
    today = date.today()
    upcoming = today + timedelta(days=7)

    # порівнюємо лише місяць і день, бо рік народження не має значення для майбутнього ДН
    contacts = db.query(Contact).filter(
        (Contact.birthday >= today) & (Contact.birthday <= upcoming)
    ).all()
    
    return contacts