from abc import ABC, abstractmethod
from enum import Enum
from .atividade import Atividade, Trabalho, Prova, Aula_de_Campo, TipoAtividade
from app.services.disciplinas_services import DisciplinaServices

class Disciplina(ABC):
    def __init__(self, nome, carga_horaria, semestre_id, codigo, observacao = None, id = None):
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.semestre_id = semestre_id
        self.atividades = []
        self.codigo = codigo
        self.observacao = observacao
        self.id = id

    def adicionar_atividade(self, atividade):
        self.atividades.append(atividade)

    def listar_atividades(self):
        for atividade in self.atividades:
            print(f"Atividade: {atividade.nome}, Data: {atividade.data}, Nota Total: {atividade.nota_total}, Observação: {atividade.observacao}")
    
    def adicionar_bd(self, conexao):
        DisciplinaServices.adicionar_bd(self, conexao)
    
    def editar_bd(self, conexao):
        DisciplinaServices.editar_bd(self, conexao)
    
    def deletar_bd(self, conexao):
        DisciplinaServices.deletar_bd(self, conexao)
    
    
    def carregar_atividades(self, conexao):
        return DisciplinaServices.carregar_atividades(self, conexao)
    
    
    