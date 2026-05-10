CREATE TABLE IF NOT EXISTS time_capsules (
  id SERIAL PRIMARY KEY,
  name VARCHAR(180), city VARCHAR(180), territory VARCHAR(180) NOT NULL,
  participant_type VARCHAR(80) NOT NULL, message TEXT NOT NULL,
  period_years INTEGER NOT NULL CHECK (period_years IN (9,14,20)),
  opening_year INTEGER NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS candidates (
  id SERIAL PRIMARY KEY,
  name VARCHAR(220) NOT NULL, email VARCHAR(220), phone VARCHAR(80),
  office VARCHAR(80) NOT NULL, city VARCHAR(180), territory VARCHAR(180),
  gender VARCHAR(80), race VARCHAR(80), photo_url TEXT,
  signed_term BOOLEAN DEFAULT FALSE, status VARCHAR(60) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS signed_terms (
  id SERIAL PRIMARY KEY,
  candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
  term_version VARCHAR(40) NOT NULL, document_hash VARCHAR(128) NOT NULL,
  ip_address VARCHAR(120), user_agent TEXT, accepted BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_capsules_territory ON time_capsules(territory);
CREATE INDEX IF NOT EXISTS idx_candidates_office ON candidates(office);
