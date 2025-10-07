from conexion.conexao import conectar

def desempenho_por_curso():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT C.nome AS curso, E.nome AS estudante, AVG(N.nota) AS media
        FROM Nota N
        JOIN Estudante E ON N.estudante_id = E.id
        JOIN Curso C ON E.curso_id = C.id
        GROUP BY C.nome, E.nome
        ORDER BY C.nome, media DESC
    """)
    resultados = cur.fetchall()
    conn.close()
    return resultados
