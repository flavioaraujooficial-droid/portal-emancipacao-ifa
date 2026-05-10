import hashlib

def term_hash(name, office, territory, version):
    raw = f'{name}|{office}|{territory}|{version}|Termo de Compromisso pela Bahia'
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()
