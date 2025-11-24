import pymongo


def get_connection():
    
    MONGO_URI = "mongodb://localhost:27017/" 
    DB_NAME = "controle_estudantes_db"
    
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        
        db.ESTUDANTE.create_index("matricula", unique=True
        
        return db
    except Exception as e:
        raise RuntimeError(f'Erro ao conectar ao MongoDB. Verifique se o servidor está rodando na URI {MONGO_URI}. Detalhe: {e}')
