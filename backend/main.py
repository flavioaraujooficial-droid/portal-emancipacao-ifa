import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

# Ajuste de importação: removendo o prefixo 'backend.' para funcionar dentro da pasta
from database import init_db
from routes.public import router as public_router
from routes.admin import router as admin_router

app = FastAPI(title='Portal Emancipação IFA', version='1.0.0')

# Configuração do Limitador (Trava de Segurança contra robôs)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Definição de Caminhos
ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / 'frontend'

# Montagem de Arquivos Estáticos
app.mount('/css', StaticFiles(directory=FRONTEND / 'css'), name='css')
app.mount('/js', StaticFiles(directory=FRONTEND / 'js'), name='js')

# Inclusão de Rotas
app.include_router(public_router)
app.include_router(admin_router)

@app.on_event('startup')
async def startup():
    # Só tenta ligar o banco se a URL existir
    if os.getenv('DATABASE_URL'):
        try:
            init_db()
            print("✅ Banco de dados sincronizado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao iniciar banco de dados: {e}")

# Rotas de Navegação (Páginas)
@app.get('/')
async def index(): return FileResponse(FRONTEND / 'index.html')

@app.get('/capsula')
async def capsula(): return FileResponse(FRONTEND / 'capsula.html')

@app.get('/termo')
async def termo(): return FileResponse(FRONTEND / 'termo.html')

@app.get('/signatarios')
async def signatarios(): return FileResponse(FRONTEND / 'signatarios.html') 

@app.get('/do-0-a-2.html')
async def do_0_a_2_html():
    return FileResponse(FRONTEND / 'do-0-a-2.html')

@app.get('/do-0-a-2')
async def do_0_a_2():
    return FileResponse(FRONTEND / 'do-0-a-2.html')

@app.get('/painel-secretario')
async def painel(): return FileResponse(FRONTEND / 'admin.html')

@app.get('/health')
async def health(): return {'status': 'operacional', 'projeto': 'IFA'}
