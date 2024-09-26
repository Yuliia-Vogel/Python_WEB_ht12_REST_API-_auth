import logging

from fastapi import APIRouter, HTTPException, Path, Depends, Query, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..schemas import ResponseContact, ContactBase, ContactUpdate, ContactCreate, ContactRead
from ..dependencies import get_token_header
from ..database import get_db
from ..repository.contact_model import Contact, User
from ..repository import contact_repo
# from ..schemas import ContactCreate, ContactRead

router = APIRouter(prefix="/contacts", tags=["contacts"])
security = HTTPBearer()


@router.get("/birthdays", response_model=list[ResponseContact]) # для пошуку днів народж. у найбл. 7 днів. Цю функцію слід ставити перед ф-цією пошуку контакту за {contact_id}, інакше фаст-апі проводить пошук саме за {contact_id}, а не днем народження
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = contact_repo.get_contacts_with_upcoming_birthdays(db)
    if not contacts:
        raise HTTPException(status_code=404, detail="No upcoming birthdays")
    return contacts


@router.get("/{contact_id}", response_model=ResponseContact) # для пошуку за id контакту
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = contact_repo.get_one_contact(db, contact_id)
    if contact:
        return contact
    raise HTTPException(status_code=404, detail="Contact not found")


@router.get("/", response_model=list[ResponseContact]) # для виведення списку всіх контактів чи для пошуку за ім'ям, прізвищем або електронною поштою (Query)
async def get_contacts(db: Session = Depends(get_db),
    first_name: str | None = Query(None), last_name: str | None = Query(None),
    email: str | None = Query(None)):
    contacts = contact_repo.get_contacts(db, first_name, last_name, email)
    return contacts
 

# @router.post("/", response_model=ResponseContact) # для створення контакту 
# async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
#     new_contact = contact_repo.create_contact(db, contact)
#     return new_contact


@router.delete("/{contact_id}") # для видалення контакту (лише через Swagger чи Postman)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact_repo.delete_contact(db, contact_id)
    return {"status": "deleted"}


@router.put("/{contact_id}", response_model=ContactUpdate) # для оновлення даних контакту (лише через Swagger чи Postman)
async def update_contact(
    contact_id: int,
    updated_contact: ContactUpdate,
    db: Session = Depends(get_db)
):
    contact = contact_repo.get_contact_by_id(db, contact_id)
    
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact.first_name = updated_contact.first_name
    contact.last_name = updated_contact.last_name
    contact.email = updated_contact.email
    contact.phone = updated_contact.phone
    contact.birthday = updated_contact.birthday
    contact.additional_info = updated_contact.additional_info

    db.commit()
    db.refresh(contact)
    
    return contact


# Створити новий контакт (лише через Swagger чи Postman) - доступно лише авториз. користувачеві
@router.post("/create_contact", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_data: ContactCreate, 
    db: Session = Depends(get_db), 
    Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()

        current_user_email = Authorize.get_jwt_subject()
        logging.info(f"Trying to authenticate user: {current_user_email}")

        user = db.query(User).filter(User.email == current_user_email).first()
        logging.info(f"User query result: {user}")


        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        logging.info(f"User ID: {user.id}")

        new_contact = Contact(**contact_data.dict(), owner_id=user.id)
        logging.info(f"New contact: {new_contact}")

        db.add(new_contact)
        logging.info(f"Contact added to database")
        
        db.commit()
        db.refresh(new_contact)

        return new_contact
    except Exception as e:
        logging.error(f"Error in create_contact: {str(e)}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))