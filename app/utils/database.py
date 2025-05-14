import os
import sqlite3
class Database:
    def __init__(self, db_path="db.db"):
        self.db_path = db_path
        self.conexao = None
        if not os.path.exists(self.db_path):
            self.__criar(script_path="app/scripts/init.sql")
        self.conexao = self.__conectar()

    def __conectar(self):
        if not self.conexao:
            self.conexao = sqlite3.connect(self.db_path)
            self.conexao.execute("PRAGMA foreign_keys = ON")
            self.cursor = self.conexao.cursor()
        return self.conexao
    
    def __criar(self, script_path):
        with open(script_path, 'r', encoding='utf-8') as script_file:
            script = script_file.read()
        
        with self.__conectar() as conexao:
            self.cursor = conexao.cursor()
            self.cursor.executescript(script)
            conexao.commit()

    def _adicionar(self, query, params):
        self.cursor.execute(query, params)
        self.conexao.commit()
        return self.cursor.lastrowid
    
    def _editar(self,query, params):
        self.cursor.execute(query, params)
        self.conexao.commit()
        return self.cursor.rowcount
    
    def _buscar_um(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def _buscar_varios(self,query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def _deletar(self, query, params):
        self.cursor.execute(query, params)
        self.conexao.commit()
        return self.cursor.rowcount