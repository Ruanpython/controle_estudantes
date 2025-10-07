from conexion.conexao import conectar
from model.curso import Curso

def inserir_curso(curso: Curso):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO Curso (nome, carga_horaria) VALUES (?, ?)", 
                (curso.nome, curso.carga_horaria))
    conn.commit()
    conn.close()

def listar_cursos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Curso")
    dados = cur.fetchall()
    conn.close()
    return dados
