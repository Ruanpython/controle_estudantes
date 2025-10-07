from conexion.conexao import conectar
from model.nota import Nota

def registrar_nota(nota: Nota):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO Nota (estudante_id, disciplina, nota) VALUES (?, ?, ?)", 
                (nota.estudante_id, nota.disciplina, nota.nota))
    conn.commit()
    conn.close()
