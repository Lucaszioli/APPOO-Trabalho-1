import os
import sqlite3
class Database:
    def __init__(self, db_path="db.db"):
        self._db_path = db_path
        self._conexao = None
        if not os.path.exists(self._db_path):
            self.__criar(script_path="app/scripts/init.sql")
        self._conexao = self.__conectar()

    def __conectar(self):
        if not self._conexao:
            self._conexao = sqlite3.connect(self._db_path)
            self._conexao.execute("PRAGMA foreign_keys = ON")
            self._cursor = self._conexao.cursor()
        return self._conexao
    
    def __criar(self, script_path):
        with open(script_path, 'r', encoding='utf-8') as script_file:
            self._script = script_file.read()
        
        with self.__conectar() as conexao:
            self._cursor = conexao.cursor()
            self._cursor.executescript(self._script)
            conexao.commit()

    def _adicionar(self, query, params):
        self._cursor.execute(query, params)
        self._conexao.commit()
        return self._cursor.lastrowid
    
    def _editar(self,query, params):
        self._cursor.execute(query, params)
        self._conexao.commit()
        return self._cursor.rowcount
    
    def _buscar_um(self, query, params):
        self._cursor.execute(query, params)
        return self._cursor.fetchone()
    
    def _buscar_varios(self,query, params):
        self._cursor.execute(query, params)
        return self._cursor.fetchall()
    
    def _deletar(self, query, params):
        self._cursor.execute(query, params)
        self._conexao.commit()
        return self._cursor.rowcount