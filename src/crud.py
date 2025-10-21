from src.db import get_connection
from src.models import Estudante, Curso, Nota


# Estudante CRUD
def criar_estudante(nome, matricula, email=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO ESTUDANTE (NOME, MATRICULA, EMAIL)
                VALUES (:nome, :matricula, :email)""", {'nome': nome, 'matricula': matricula, 'email': email})
    conn.commit()
    cur.close()
    conn.close()

def listar_estudantes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_ESTUDANTE, NOME, MATRICULA, EMAIL FROM ESTUDANTE ORDER BY ID_ESTUDANTE")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [Estudante(id=r[0], nome=r[1], matricula=r[2], email=r[3]) for r in rows]

def atualizar_estudante(id_estudante, nome=None, matricula=None, email=None):
    conn = get_connection()
    cur = conn.cursor()
    updates = []
    params = {}
    if nome is not None:
        updates.append('NOME = :nome'); params['nome']=nome
    if matricula is not None:
        updates.append('MATRICULA = :matricula'); params['matricula']=matricula
    if email is not None:
        updates.append('EMAIL = :email'); params['email']=email
    if not updates:
        cur.close(); conn.close(); return
    sql = 'UPDATE ESTUDANTE SET ' + ', '.join(updates) + ' WHERE ID_ESTUDANTE = :id'
    params['id'] = id_estudante
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()

def excluir_estudante(id_estudante):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM ESTUDANTE WHERE ID_ESTUDANTE = :id', {'id': id_estudante})
    conn.commit()
    cur.close()
    conn.close()

# Curso CRUD
def criar_curso(nome, carga_horaria=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO CURSO (NOME, CARGA_HORARIA) VALUES (:nome, :ch)', {'nome': nome, 'ch': carga_horaria})
    conn.commit()
    cur.close()
    conn.close()

def listar_cursos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT ID_CURSO, NOME, CARGA_HORARIA FROM CURSO ORDER BY ID_CURSO')
    rows = cur.fetchall()
    cur.close(); conn.close()
    return [Curso(id=r[0], nome=r[1], carga_horaria=r[2]) for r in rows]

def atualizar_curso(id_curso, nome=None, carga_horaria=None):
    conn = get_connection()
    cur = conn.cursor()
    updates = []; params={}
    if nome is not None:
        updates.append('NOME = :nome'); params['nome']=nome
    if carga_horaria is not None:
        updates.append('CARGA_HORARIA = :ch'); params['ch']=carga_horaria
    if not updates:
        cur.close(); conn.close(); return
    sql = 'UPDATE CURSO SET ' + ', '.join(updates) + ' WHERE ID_CURSO = :id'
    params['id'] = id_curso
    cur.execute(sql, params)
    conn.commit()
    cur.close(); conn.close()

def excluir_curso(id_curso):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM CURSO WHERE ID_CURSO = :id', {'id': id_curso})
    conn.commit(); cur.close(); conn.close()

# Nota CRUD
def lancar_nota(id_estudante, id_curso, nota1=None, nota2=None):
    media = None
    if nota1 is not None and nota2 is not None:
        media = round((float(nota1) + float(nota2)) / 2, 2)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO NOTA (ID_ESTUDANTE, ID_CURSO, NOTA1, NOTA2, MEDIA) VALUES (:e, :c, :n1, :n2, :m)',
                {'e': id_estudante, 'c': id_curso, 'n1': nota1, 'n2': nota2, 'm': media})
    conn.commit(); cur.close(); conn.close()

def listar_notas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT n.ID_NOTA, n.ID_ESTUDANTE, e.NOME, n.ID_CURSO, c.NOME, n.NOTA1, n.NOTA2, n.MEDIA
                   FROM NOTA n
                   JOIN ESTUDANTE e ON e.ID_ESTUDANTE = n.ID_ESTUDANTE
                   JOIN CURSO c ON c.ID_CURSO = n.ID_CURSO
                   ORDER BY n.ID_NOTA''')
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def atualizar_nota(id_nota, nota1=None, nota2=None):
    conn = get_connection()
    cur = conn.cursor()
    # calcular nova média se necessário
    cur.execute('SELECT NOTA1, NOTA2 FROM NOTA WHERE ID_NOTA = :id', {'id': id_nota})
    r = cur.fetchone()
    if not r:
        cur.close(); conn.close(); return False
    n1 = nota1 if nota1 is not None else r[0]
    n2 = nota2 if nota2 is not None else r[1]
    media = None
    if n1 is not None and n2 is not None:
        media = round((float(n1) + float(n2)) / 2, 2)
    updates = []
    params = {}
    if nota1 is not None:
        updates.append('NOTA1 = :n1'); params['n1'] = nota1
    if nota2 is not None:
        updates.append('NOTA2 = :n2'); params['n2'] = nota2
    updates.append('MEDIA = :m'); params['m'] = media
    params['id'] = id_nota
    sql = 'UPDATE NOTA SET ' + ', '.join(updates) + ' WHERE ID_NOTA = :id'
    cur.execute(sql, params)
    conn.commit(); cur.close(); conn.close()
    return True

def excluir_nota(id_nota):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM NOTA WHERE ID_NOTA = :id', {'id': id_nota})
    conn.commit(); cur.close(); conn.close()

# Relatórios
def relatorio_desempenho_por_estudante(id_estudante):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT c.NOME, n.NOTA1, n.NOTA2, n.MEDIA,
                          CASE WHEN n.MEDIA >= 6 THEN 'APROVADO' ELSE 'REPROVADO' END AS SITUACAO
                   FROM NOTA n JOIN CURSO c ON c.ID_CURSO = n.ID_CURSO
                   WHERE n.ID_ESTUDANTE = :id''', {'id': id_estudante})
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def relatorio_media_por_curso(id_curso):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT AVG(n.MEDIA) FROM NOTA n WHERE n.ID_CURSO = :id''', {'id': id_curso})
    r = cur.fetchone(); cur.close(); conn.close()
    return r[0] if r else None
