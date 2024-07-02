from fastapi_login import LoginManager
from config import SECRET, DB_ADDRESS
import psycopg2

manager = LoginManager(SECRET, token_url='/auth/token')


def get_data(model):
    with psycopg2.connect(DB_ADDRESS) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE access_token=%s", (model.access_token,))
        conn.commit()
    
    lines = cursor.fetchone()
    cursor.close()
    
    return lines


# Função para carregar o usuário do banco de dados
@manager.user_loader()
def load_user(email: str):
    with psycopg2.connect(DB_ADDRESS) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        
    conn.commit()
    cursor.close()
    
    return user