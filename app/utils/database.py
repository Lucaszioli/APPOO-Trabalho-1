import sqlite3
class Database:
    def __init__(self, db_path="db.db"):
        self.db_path = db_path

    def conectar(self):
        return sqlite3.connect(self.db_path)
    
    def criar(self, script_path):
        with open(script_path, 'r', encoding='utf-8') as script_file:
            script = script_file.read()
        
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.executescript(script)
            conexao.commit()