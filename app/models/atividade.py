from abc import ABC, abstractmethod
from enum import Enum

class TipoAtividade(Enum):
    TRABALHO = "Trabalho"
    PROVA = "Prova"
    CAMPO = "Aula de campo"
    APRESENTACAO = "Apresentação de Trabalho"
    REVISAO = "Aula de revisão"

class Atividade:
    def __init__(self):
        pass