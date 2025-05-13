import sqlite3
class Database:
    def __init__(self, db_path="db.db"):
        self.db_path = db_path
        self.conexao = None
        self.__criar(script_path="app/scripts/init.sql")
        self.conexao = self.__conectar()

    def __conectar(self):
        if not self.conexao:
            self.conexao = sqlite3.connect(self.db_path)
            self.conexao.execute("PRAGMA foreign_keys = ON")
        return self.conexao
    
    def __criar(self, script_path):
        with open(script_path, 'r', encoding='utf-8') as script_file:
            script = script_file.read()
        
        with self.__conectar() as conexao:
            cursor = conexao.cursor()
            cursor.executescript(script)
            conexao.commit()

    @staticmethod
    def _adicionar(query, params, conexao):
        cursor = conexao.cursor()
        cursor.execute(query, params)
        conexao.commit()
        return cursor.lastrowid
    
    @staticmethod
    def _editar(query, params, conexao):
        cursor = conexao.cursor()
        cursor.execute(query, params)
        conexao.commit()
        return cursor.rowcount
    
    @staticmethod
    def _buscar_um(query, params, conexao):
        cursor = conexao.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return row
    
    @staticmethod
    def _buscar_varios(query, params, conexao):
        cursor = conexao.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    
    @staticmethod
    def _deletar(query, params, conexao):
        cursor = conexao.cursor()
        cursor.execute(query, params)
        conexao.commit()
        return cursor.rowcount