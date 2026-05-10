import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from database import init_db
from routes.public import router as public_router
from routes.admin import router as admin_router

app = FastAPI(title='Portal Emancipação IFA', version='1.0.0')
app.state.limiter = Limiter(key_func=get_remote_address)
app.add_middleware(SlowAPIMiddleware)

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / 'frontend'
app.mount('/css', StaticFiles(directory=FRONTEND / 'css'), name='css')
app.mount('/js', StaticFiles(directory=FRONTEND / 'js'), name='js')
app.include_router(public_router)
app.include_router(admin_router)

@app.on_event('startup')
def startup():
    if os.getenv('DATABASE_URL'):
        init_db()

@app.get('/')
async def index(): return FileResponse(FRONTEND / 'index.html')
@app.get('/capsula')
async def capsula(): return FileResponse(FRONTEND / 'capsula.html')
@app.get('/termo')
async def termo(): return FileResponse(FRONTEND / 'termo.html')
@app.get('/signatarios')
async def signatarios(): return FileResponse(FRONTEND / 'signatarios.html')
@app.get('/painel-secretario')
async def painel(): return FileResponse(FRONTEND / 'admin.html')
@app.get('/health')
async def health(): return {'ok': True}
