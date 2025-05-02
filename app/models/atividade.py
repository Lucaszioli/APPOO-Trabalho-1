from abc import ABC, abstractmethod
from enum import Enum

class TipoAtividade(Enum):
    TRABALHO = "Trabalho"
    PROVA = "Prova"
    CAMPO = "Aula de campo"
    APRESENTACAO = "Apresentação de Trabalho"
    REVISAO = "Aula de revisão"

class Atividade:
    def __init__(self, nome, data, id_disciplina, observacoes = None):
        self.nome = nome
        self.data = data
        self.id_disciplina = id_disciplina
        self.observacoes = observacoes
        pass


class Trabalho(Atividade):
    def __init__(self, nome, data, id_disciplina, nota_maxima, nota = None, observacoes = None):
        super().__init__(nome, data, id_disciplina, observacoes)
        self.tipo = TipoAtividade.TRABALHO
        self.nota_maxima = nota_maxima
        self.nota = nota

class Prova(Atividade):
    def __init__(self, nome, data, id_disciplina, nota_maxima, nota = None, observacoes = None):
        super().__init__(nome, data, id_disciplina, observacoes)
        self.tipo = TipoAtividade.PROVA
        self.nota_maxima = nota_maxima
        self.nota = nota

class Aula_de_Campo(Atividade):
    def __init__(self, nome, data, id_disciplina, observacoes = None):
        super().__init__(nome, data, id_disciplina, observacoes)
        self.tipo = TipoAtividade.CAMPO

class Apresentacao(Atividade):
    def __init__(self, nome, data, id_disciplina, nota_maxima, nota = None, observacoes = None):
        super().__init__(nome, data, id_disciplina, observacoes)
        self.tipo = TipoAtividade.APRESENTACAO
        self.nota_maxima = nota_maxima
        self.nota = nota


class Revisao(Atividade):
    def __init__(self, nome, data, id_disciplina, observacoes = None, nota = None):
        super().__init__(nome, data, id_disciplina, observacoes)
        self.tipo = TipoAtividade.REVISAO
        self.nota = nota