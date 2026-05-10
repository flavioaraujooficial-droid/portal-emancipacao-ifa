from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from database import get_connection
from auth import authenticate_admin, create_admin_token, require_admin

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post('/api/admin/login')
@limiter.limit('5/minute')
async def admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if not authenticate_admin(username, password):
        return JSONResponse({'ok': False, 'message': 'Credenciais inválidas.'}, status_code=401)
    token = create_admin_token(username)
    response = JSONResponse({'ok': True})
    response.set_cookie('ifa_admin_session', token, httponly=True, secure=True, samesite='strict', max_age=8*60*60)
    return response

@router.get('/api/admin/dashboard')
async def dashboard(request: Request):
    require_admin(request)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM time_capsules ORDER BY created_at DESC LIMIT 200')
            capsules = cur.fetchall()
            cur.execute('SELECT * FROM candidates ORDER BY created_at DESC LIMIT 200')
            candidates = cur.fetchall()
            cur.execute('SELECT territory, COUNT(*) AS total FROM time_capsules GROUP BY territory ORDER BY total DESC LIMIT 50')
            territories = cur.fetchall()
    return {'capsules': capsules, 'candidates': candidates, 'territories': territories}
