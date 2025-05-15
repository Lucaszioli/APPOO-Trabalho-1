from abc import ABC, abstractmethod
from enum import Enum

class TipoAtividade(Enum):
    TRABALHO = "Trabalho"
    PROVA = "Prova"
    CAMPO = "Aula de campo"
    REVISAO = "Aula de revisão"

class Atividade(ABC):
    def __init__(self, nome, data, disciplina_id, observacao = None, id=None):
        self.id = id
        self.nome = nome
        self.data = data
        self.disciplina_id = disciplina_id
        self.observacao = observacao


    @abstractmethod
    def adicionar_bd(self, conexao):
        pass


class Trabalho(Atividade):
    def __init__(self, nome, data, disciplina_id, nota_total, data_apresentacao = None, nota = None, observacao = None, id=None):
        super().__init__(nome, data, disciplina_id, observacao, id)
        self.tipo = TipoAtividade.TRABALHO
        self.nota_total = nota_total
        self.nota = nota
        self.data_apresentacao = data_apresentacao

    def adicionar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO atividade (nome, data, disciplina_id, tipo, nota_total, nota, observacao, data_apresentacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (self.nome, self.data, self.disciplina_id, self.tipo.value, self.nota_total, self.nota, self.observacao, self.data_apresentacao))
        conexao.commit()
        self.id = cursor.lastrowid
        

class Prova(Atividade):
    def __init__(self, nome, data, disciplina_id, nota_total, nota = None, observacao = None, id=None):
        super().__init__(nome, data, disciplina_id, observacao, id)
        self.tipo = TipoAtividade.PROVA
        self.nota_total = nota_total
        self.nota = nota

    def adicionar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO atividade (nome, data, disciplina_id, tipo, nota_total, nota, observacao) VALUES (?, ?, ?, ?, ?, ?, ?)", (self.nome, self.data, self.disciplina_id, self.tipo.value, self.nota_total, self.nota, self.observacao))
        conexao.commit()
        self.id = cursor.lastrowid

class Aula_de_Campo(Atividade):
    def __init__(self, nome, data, disciplina_id, lugar, observacao = None, id=None):
        super().__init__(nome, data, disciplina_id, observacao, id)
        self.tipo = TipoAtividade.CAMPO
        self.lugar = lugar

    def adicionar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO atividade (nome, data, disciplina_id, tipo, observacao, lugar) VALUES (?, ?, ?, ?, ?,?)", (self.nome, self.data, self.disciplina_id, self.tipo.value, self.observacao, self.lugar))
        conexao.commit()
        self.id = cursor.lastrowid

class Revisao(Atividade):
    def __init__(self, nome, data, disciplina_id, observacao = None, id=None):
        super().__init__(nome, data, disciplina_id, observacao, id)
        self.tipo = TipoAtividade.REVISAO

    def adicionar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO atividade (nome, data, disciplina_id, tipo, nota, observacao) VALUES (?, ?, ?, ?, ?, ?)", (self.nome, self.data, self.disciplina_id, self.tipo.value, self.nota, self.observacao))
        conexao.commit()
        self.id = cursor.lastrowid
        