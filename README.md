# Python_WEB_ht12_REST_API_auth
RESTful API with registration, authorization and authentification.

1. Create and activate venv
2. pip install poetry
3. poetry install --no-root
4. pip install passlib==1.7.4 bcrypt==3.2.0 
5. uvicorn app.main:app --reload
6. auth/signup
7. auth/login -> copy token
8. "Authorize" button at the right top corner of page -> paste token -> Authorize -> Close
9. POST. Create Contact -> fill in information about contact -> execute.
10. Edit (PUT), Delete - only owner can perform.
11. To stop application - CTRL+C 











fastapi-jwt-auth ще не підтримує Pydantic версії 2, і виникає конфлікт через несумісність змін між Pydantic 1.x і 2.x, а саме використання декораторів валідації. Справа в тому, що я використовую gfrtn fastapi, який використовує pydantic 2x, де змінилися деякі принципи роботи з валідацією. У версії 2 Pydantic видалив @validator, як це працювало у версії 1, і замінив його на новий механізм @field_validator. 
-->   pydantic = "<2.0.0"  # Додаємо обмеження на версію Pydantic