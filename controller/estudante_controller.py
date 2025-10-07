from conexion.conexao import conectar
from model.estudante import Estudante

def inserir_estudante(estudante: Estudante):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO Estudante (nome, matricula, curso_id) VALUES (?, ?, ?)", 
                (estudante.nome, estudante.matricula, estudante.curso_id))
    conn.commit()
    conn.close()

def listar_estudantes():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT E.id, E.nome, E.matricula, C.nome 
        FROM Estudante E 
        LEFT JOIN Curso C ON E.curso_id = C.id
    """)
    dados = cur.fetchall()
    conn.close()
    return dados
