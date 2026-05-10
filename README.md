# Portal Emancipação IFA — MVP Fase 1

Plataforma pública de Cápsula do Tempo, Termo de Compromisso pela Bahia e lista transparente de signatários.

## Módulos
- Home pública
- Cápsula do Tempo
- Termo de Compromisso
- Assinatura auditável de candidatos
- Lista pública por cargo
- Painel administrativo básico
- FastAPI + PostgreSQL + Render

## Variáveis de ambiente
Configure no Render:

```env
DATABASE_URL=
ADMIN_USER=
ADMIN_PASSWORD=
JWT_SECRET=
TERM_VERSION=2026.1
```

Nunca suba `.env` para o GitHub.
