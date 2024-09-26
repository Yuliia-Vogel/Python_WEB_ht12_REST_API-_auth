from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from fastapi import APIRouter

from .routers import contacts, auth
from .config import settings
from .database import engine, Base # для того, щоб тут підключитися до Постгресу й створити таблиці(якщо їх ще немає)

app = FastAPI() # створюю основний додаток

origins = [
    "http://localhost:3000",
    "localhost:3000"
] # це для фронту, це список, звідки можна стукатися, тут описаний локалхот 3000, це той, який має node-додаток
# (він тут є зі схемою і без схеми)


app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
) # ососбливо важливо тут CORS

# створюю мою таблицю в постгресі перед запуском сервера (якщо таблиця вже є, то й ок, нічого не трапиться, це безпечно)
Base.metadata.create_all(bind=engine)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

# Налаштування JWT
@AuthJWT.load_config
def get_config():
    return settings


app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


@app.get("/") 
async def root(): # привітальне повідомлення за адресою http://127.0.0.1:8000/
    return {
        "message": "Hello Contact API",
        "status": "Ok"
    }

# Кастомізація OpenAPI для включення Bearer авторизації
def custom_openapi():
    if app.openapi_schema:
        print("OpenAPI schema entered -if-")
        return app.openapi_schema
    # openapi_schema = original_openapi()
    openapi_schema = get_openapi(
        title="Python WEB HW12 - Yuliia Melnychenko",
        version="1.0.0",
        description="Contact FAST API with auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

test_router = APIRouter()

@test_router.get("/test", tags=["Test"])
async def test_route():
    return {"message": "This is a test route",
    "status": "Ok"
    }

app.include_router(test_router, prefix="/api")