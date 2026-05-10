import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Request, HTTPException

JWT_SECRET = os.getenv('JWT_SECRET', 'dev-change')
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
ALGORITHM = 'HS256'

def authenticate_admin(username, password):
    return username == ADMIN_USER and password == ADMIN_PASSWORD

def create_admin_token(username):
    payload = {'sub': username, 'role': 'admin', 'exp': datetime.utcnow() + timedelta(hours=8)}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

def require_admin(request: Request):
    token = request.cookies.get('ifa_admin_session')
    if not token:
        raise HTTPException(status_code=401, detail='Sessão não encontrada.')
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        if payload.get('role') != 'admin':
            raise HTTPException(status_code=403, detail='Acesso negado.')
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail='Sessão inválida.')
