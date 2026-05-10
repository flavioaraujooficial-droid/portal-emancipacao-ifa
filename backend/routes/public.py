import os
from fastapi import APIRouter, Request, Form, HTTPException
from database import get_connection
from backend.services.audit import term_hash

router = APIRouter()
VALID_PERIODS = {9,14,20}
OFFICES = {'governador','senado','deputado_federal','deputado_estadual'}

@router.post('/api/capsules')
async def create_capsule(name: str = Form(''), city: str = Form(''), territory: str = Form(...), participant_type: str = Form(...), message: str = Form(...), period_years: int = Form(...)):
    if period_years not in VALID_PERIODS:
        raise HTTPException(status_code=400, detail='Prazo inválido.')
    opening_year = 2027 + period_years
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''INSERT INTO time_capsules (name, city, territory, participant_type, message, period_years, opening_year) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id, opening_year''', (name, city, territory, participant_type, message, period_years, opening_year))
            row = cur.fetchone()
    return {'ok': True, 'id': row['id'], 'opening_year': row['opening_year']}

@router.post('/api/candidates/sign')
async def sign_term(request: Request, name: str = Form(...), email: str = Form(''), phone: str = Form(''), office: str = Form(...), city: str = Form(''), territory: str = Form(...), gender: str = Form(''), race: str = Form(''), photo_url: str = Form(''), accept_term: str = Form(...)):
    if office not in OFFICES:
        raise HTTPException(status_code=400, detail='Cargo inválido.')
    if accept_term.lower() not in {'sim','true','on','1','aceito'}:
        raise HTTPException(status_code=400, detail='O termo precisa ser aceito.')
    version = os.getenv('TERM_VERSION', '2026.1')
    ip = request.client.host if request.client else ''
    ua = request.headers.get('user-agent','')
    doc_hash = term_hash(name, office, territory, version)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''INSERT INTO candidates (name,email,phone,office,city,territory,gender,race,photo_url,signed_term,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE,'signed') RETURNING id''', (name,email,phone,office,city,territory,gender,race,photo_url))
            candidate = cur.fetchone()
            cur.execute('''INSERT INTO signed_terms (candidate_id, term_version, document_hash, ip_address, user_agent, accepted) VALUES (%s,%s,%s,%s,%s,TRUE)''', (candidate['id'], version, doc_hash, ip, ua))
    return {'ok': True, 'candidate_id': candidate['id'], 'hash': doc_hash}

@router.get('/api/signatories')
async def signatories():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT c.id,c.name,c.office,c.city,c.territory,c.gender,c.race,c.photo_url,c.status,c.created_at,st.term_version,st.document_hash FROM candidates c LEFT JOIN signed_terms st ON st.candidate_id=c.id WHERE c.signed_term=TRUE ORDER BY c.office,c.created_at DESC''')
            rows = cur.fetchall()
    return {'items': rows}

@router.get('/api/public-stats')
async def public_stats():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) AS total FROM time_capsules')
            capsules = cur.fetchone()['total']
            cur.execute('SELECT COUNT(*) AS total FROM candidates WHERE signed_term=TRUE')
            signatories = cur.fetchone()['total']
            cur.execute('SELECT COUNT(DISTINCT territory) AS total FROM time_capsules')
            territories = cur.fetchone()['total']
    return {'capsules': capsules, 'signatories': signatories, 'territories': territories}
