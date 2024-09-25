from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from fastapi import APIRouter

from .routers import contacts, auth
from .config import settings
from .database import engine, Base # для того, щоб тут підключитися до Постгресу й створити таблиці(якщо їх ще немає)

app = FastAPI() # створюю основний додаток

# app.openapi_schema = None

# app.openapi_schema = {
#     "components": {
#         "securitySchemes": {
#             "BearerAuth": {
#                 "type": "http",
#                 "scheme": "bearer",
#                 "bearerFormat": "JWT",
#             }
#         }
#     },
#     "security": [{"BearerAuth": []}],
# }

origins = [
    "http://localhost:3000",
    "localhost:3000"
] # це для фронту, це список, звідки можна стукатися, тут описаний локалхот 3000, це той, який має node-додаток
# (він тут є зі схемою і без схеми)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
) # для фронту, ососбливо важливо тут CORSMiddleware


# створюю мою таблицю в постгресі перед запуском сервера (якщо таблиця вже є, то й ок, нічого не трапиться, це безпечно)
Base.metadata.create_all(bind=engine)



# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = app.openapi()
#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#         }
#     }
#     openapi_schema["security"] = [{"BearerAuth": []}]
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi


# Налаштування JWT
@AuthJWT.load_config
def get_config():
    return settings


app.include_router(auth.router)
app.include_router(contacts.router, prefix="/api")


@app.get("/") 
async def root(): # привітальне повідомлення за адресою http://127.0.0.1:8000/
    return {
        "message": "Hello Contact API",
        "status": "Ok"
    }

# Кастомізація OpenAPI для включення Bearer авторизації
# @app.get("/openapi.json", include_in_schema=False)
# async def custom_openapi():
#     openapi_schema = app.openapi()
#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#         }
#     }
#     openapi_schema["security"] = [{"BearerAuth": []}]
#     return openapi_schema
original_openapi = app.openapi

# Кастомізація OpenAPI для включення Bearer авторизації
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = original_openapi()
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# app.openapi = custom_openapi

test_router = APIRouter()

@test_router.get("/test", tags=["Test"])
async def test_route():
    return {"message": "This is a test route",
    "status": "Ok"
    }

app.include_router(test_router, prefix="/api")