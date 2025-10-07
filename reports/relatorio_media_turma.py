from conexion.conexao import conectar

def media_por_turma():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT C.nome AS curso, AVG(N.nota) AS media
        FROM Nota N
        JOIN Estudante E ON N.estudante_id = E.id
        JOIN Curso C ON E.curso_id = C.id
        GROUP BY C.nome
    """)
    resultados = cur.fetchall()
    conn.close()
    return resultados
