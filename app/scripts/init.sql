CREATE TABLE IF NOT EXISTS semestre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_inicio TEXT NOT NULL,
    data_fim TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS disciplina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    codigo TEXT NOT NULL,
    carga_horaria INTEGER NOT NULL,
    semestre_id INTEGER NOT NULL,
    observacao TEXT,
    FOREIGN KEY (semestre_id) REFERENCES semestre(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS atividade(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data TEXT NOT NULL,
    nota REAL,
    nota_total REAL,
    disciplina_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    observacao TEXT,
    FOREIGN KEY (disciplina_id) REFERENCES disciplina(id) ON DELETE CASCADE
);