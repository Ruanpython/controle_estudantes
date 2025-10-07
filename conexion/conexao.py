import sqlite3

def conectar():
    return sqlite3.connect("controle_estudantes.db")

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Curso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        carga_horaria INTEGER
    );

    CREATE TABLE IF NOT EXISTS Estudante (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        matricula TEXT UNIQUE NOT NULL,
        curso_id INTEGER,
        FOREIGN KEY (curso_id) REFERENCES Curso(id)
    );

    CREATE TABLE IF NOT EXISTS Nota (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estudante_id INTEGER,
        disciplina TEXT,
        nota REAL,
        FOREIGN KEY (estudante_id) REFERENCES Estudante(id)
    );
    """)
    conexao.commit()
    conexao.close()
