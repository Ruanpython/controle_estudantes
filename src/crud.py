from src.db import get_connection
from src.models import Estudante, Curso, CursoEmbed
from typing import List

def calcular_media_situacao(n1, n2):
    media = None
    situacao = None
    if n1 is not None and n2 is not None:
        media = round((float(n1) + float(n2)) / 2, 2)
        situacao = 'APROVADO' if media >= 6.0 else 'REPROVADO'
    return media, situacao

def get_next_id(db, collection_name, id_field):
    
    doc = db[collection_name].find({}).sort([(id_field, -1)]).limit(1)
    if doc.count() > 0:
        return doc[0].get(id_field, 0) + 1
    return 1



def criar_estudante(nome, matricula, email=None):
    db = get_connection()
    new_id = get_next_id(db, 'ESTUDANTE', 'id_estudante')
    estudante_doc = {
        'id_estudante': new_id,
        'nome': nome,
        'matricula': matricula,
        'email': email,
        'cursos': []
    }
    db.ESTUDANTE.insert_one(estudante_doc)

def listar_estudantes() -> List[Estudante]:
    db = get_connection()
    rows = db.ESTUDANTE.find().sort('id_estudante', 1)
    estudantes = []
    for r in rows:
        cursos_embed = [CursoEmbed(**c) for c in r.get('cursos', [])]
        estudantes.append(Estudante(id=r['id_estudante'], nome=r['nome'], matricula=r['matricula'], email=r['email'], cursos=cursos_embed))
    return estudantes

def atualizar_estudante(id_estudante, nome=None, matricula=None, email=None):
    db = get_connection()
    update_data = {}
    if nome is not None:
        update_data['nome'] = nome
    if matricula is not None:
        update_data['matricula'] = matricula
    if email is not None:
        update_data['email'] = email
        
    if update_data:
        db.ESTUDANTE.update_one({'id_estudante': id_estudante}, {'$set': update_data})

def excluir_estudante(id_estudante):
    db = get_connection()
    db.ESTUDANTE.delete_one({'id_estudante': id_estudante})



def criar_curso(nome, carga_horaria=None):
    db = get_connection()
    new_id = get_next_id(db, 'CURSO', 'id_curso')
    curso_doc = {'id_curso': new_id, 'nome': nome, 'carga_horaria': carga_horaria}
    db.CURSO.insert_one(curso_doc)

def listar_cursos() -> List[Curso]:
    db = get_connection()
    rows = db.CURSO.find().sort('id_curso', 1)
    return [Curso(id=r['id_curso'], nome=r['nome'], carga_horaria=r.get('carga_horaria')) for r in rows]

def atualizar_curso(id_curso, nome=None, carga_horaria=None):
    db = get_connection()
    update_data = {}
    if nome is not None:
        update_data['nome'] = nome
    if carga_horaria is not None:
        update_data['carga_horaria'] = carga_horaria
        
    if update_data:
        
        db.CURSO.update_one({'id_curso': id_curso}, {'$set': update_data})
        
        
        if nome is not None:
             db.ESTUDANTE.update_many(
                {'cursos.id_curso': id_curso},
                {'$set': {'cursos.$[elem].nome_curso': nome}},
                array_filters=[{'elem.id_curso': id_curso}]
            )

def excluir_curso(id_curso):
    db = get_connection()
    db.CURSO.delete_one({'id_curso': id_curso})
    db.ESTUDANTE.update_many({}, {'$pull': {'cursos': {'id_curso': id_curso}}})

def lancar_nota(id_estudante, id_curso, nota1=None, nota2=None):
    db = get_connection()
    
    existe = db.ESTUDANTE.find_one({'id_estudante': id_estudante, 'cursos.id_curso': id_curso})
    if existe:
        print("Erro: Nota para este curso e estudante já existe. Use 'Atualizar nota'.")
        return
        
    media, situacao = calcular_media_situacao(nota1, nota2)
    curso_master = db.CURSO.find_one({'id_curso': id_curso})
    if not curso_master: return # Curso não existe
    

    curso_embed = {
        'id_curso': id_curso,
        'nome_curso': curso_master['nome'],
        'carga_horaria': curso_master['carga_horaria'],
        'nota1': nota1,
        'nota2': nota2,
        'media': media,
        'situacao': situacao
    }
    

    db.ESTUDANTE.update_one(
        {'id_estudante': id_estudante},
        {'$push': {'cursos': curso_embed}}
    )

def listar_notas():
    db = get_connection()
    pipeline = [
        {'$unwind': '$cursos'},
        {'$project': {
            '_id': 0, 
            'ID_ESTUDANTE': '$id_estudante',
            'NOME_ESTUDANTE': '$nome',
            'ID_CURSO': '$cursos.id_curso',
            'NOME_CURSO': '$cursos.nome_curso',
            'NOTA1': '$cursos.nota1',
            'NOTA2': '$cursos.nota2',
            'MEDIA': '$cursos.media'
        }},
        {'$sort': {'ID_ESTUDANTE': 1, 'ID_CURSO': 1}}
    ]
    return list(db.ESTUDANTE.aggregate(pipeline)) 

def atualizar_nota(id_estudante, id_curso, nota1=None, nota2=None):
    db = get_connection()
    
    estudante = db.ESTUDANTE.find_one(
        {'id_estudante': id_estudante, 'cursos.id_curso': id_curso},
        {'cursos.$': 1, '_id': 0}
    )
    
    if not estudante or not estudante.get('cursos'):
        return False
        
    curso_atual = estudante['cursos'][0]
    n1 = nota1 if nota1 is not None else curso_atual.get('nota1')
    n2 = nota2 if nota2 is not None else curso_atual.get('nota2')
    media, situacao = calcular_media_situacao(n1, n2)


    update_data = {}
    if nota1 is not None: update_data['cursos.$.nota1'] = n1
    if nota2 is not None: update_data['cursos.$.nota2'] = n2
    update_data['cursos.$.media'] = media
    update_data['cursos.$.situacao'] = situacao

 
    result = db.ESTUDANTE.update_one(
        {'id_estudante': id_estudante, 'cursos.id_curso': id_curso},
        {'$set': update_data}
    )
    return result.modified_count > 0

def excluir_nota(id_estudante, id_curso):
    db = get_connection()
    result = db.ESTUDANTE.update_one(
        {'id_estudante': id_estudante},
        {'$pull': {'cursos': {'id_curso': id_curso}}}
    )
    return result.modified_count > 0

def relatorio_desempenho_por_estudante(id_estudante):
    db = get_connection()
    pipeline = [
        {'$match': {'id_estudante': id_estudante}},
        {'$unwind': '$cursos'},
        {'$project': {
            '_id': 0, 
            'NOME_CURSO': '$cursos.nome_curso',
            'NOTA1': '$cursos.nota1',
            'NOTA2': '$cursos.nota2',
            'MEDIA': '$cursos.media',
            'SITUACAO': '$cursos.situacao'
        }},
        {'$sort': {'NOME_CURSO': 1}}
    ]
    return list(db.ESTUDANTE.aggregate(pipeline))

def relatorio_media_por_curso(id_curso):
    db = get_connection()
    pipeline = [
        {'$unwind': '$cursos'},
        {'$match': {'cursos.id_curso': id_curso}},
        {'$group': {
            '_id': '$cursos.id_curso',
            'media_geral': {'$avg': '$cursos.media'}
        }}
    ]
    result = list(db.ESTUDANTE.aggregate(pipeline))
    if result and 'media_geral' in result[0]:
        return round(result[0]['media_geral'], 2)
    return None
