import oracledb as cx_Oracle
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
section = config['oracle']

def get_connection():
    user = section.get('user')
    password = section.get('password')
    dsn = section.get('dsn')
    if not all([user, password, dsn]):
        raise RuntimeError('Preencha config.ini com user, password e dsn.')
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    return conn
