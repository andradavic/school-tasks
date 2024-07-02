from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from app.validadores.email import validate_email
from app.basemodel.types import LogoutModel
from app.basemodel.auth import *
import psycopg2

router = APIRouter()
manager = LoginManager(SECRET, token_url='/auth/token')

# Rota para authenticate
@router.post("/login")
def login(device_name: str, data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)

    if not user:
        raise InvalidCredentialsException
    elif password != user[3]:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data=dict(sub=email))

    with psycopg2.connect(DB_ADDRESS) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO devices (user_id, device_name, access_token) VALUES (%s, %s, %s)",
                       (user[0], device_name, access_token))
        conn.commit()

    cursor.close()
    return {
        'access_token': access_token,
    }


@router.post("/signup")
def signup(data: OAuth2PasswordRequestForm = Depends()):
    try:
        validate_email(data.username)

    except:
        raise HTTPException(status_code=401, detail="Invalid email")

    email = data.username
    username = data.username
    password = data.password

    user = load_user(email)

    if user:
        raise HTTPException(status_code=444, detail="Username already exists")

    if len(password) < 8:
        raise HTTPException(status_code=408, detail="Password must be longer than 8 characters")
    elif len(password) > 20:
        raise HTTPException(status_code=420, detail="Password must be no longer than 20 characters")

    with psycopg2.connect(DB_ADDRESS) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()

    cursor.close()


@router.post("/logout")
def logout(data: LogoutModel = Depends()):
    with psycopg2.connect(DB_ADDRESS) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM devices WHERE access_token=%s", (data.access_token,))
        token = cursor.fetchone()
        if not token:
            return {
                "status": "not found"
            }
        cursor.execute("DELETE FROM devices WHERE access_token=%s", (data.access_token,))
        conn.commit()
        cursor.close()
        
    return {
        "status": "disconnected"
    }
