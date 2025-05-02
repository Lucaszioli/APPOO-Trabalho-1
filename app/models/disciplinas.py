from abc import ABC, abstractmethod
from enum import Enum
from atividade import Trabalho, Prova, Aula_de_Campo, Apresentacao

class Disciplina(ABC):
    def __init__(self, nome, carga_horaria, semestre_id, observacao = None, id = None):
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.semestre_id = semestre_id
        self.atividades = []
        self.observacao = observacao
        self.id = id
        pass

    def adicionar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO disciplina (nome, carga_horaria, semestre_id, observacao) VALUES (?, ?, ?, ?)", (self.nome, self.carga_horaria, self.semestre_id, self.observacao))
        conexao.commit()
        self.id = cursor.lastrowid()
        pass
    
    def editar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("UPDATE disciplina SET nome = ?, carga_horaria = ?, semestre_id = ?, observacao = ? WHERE id = ?", (self.nome, self.carga_horaria, self.semestre_id, self.observacao, self.id))
        conexao.commit()
        pass
    
    def deletar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM disciplina WHERE id = ?", (self.id,))
        conexao.commit()
        pass
    
    def adicionar_atividade(self, atividade):
        self.atividades.append(atividade)
    
    