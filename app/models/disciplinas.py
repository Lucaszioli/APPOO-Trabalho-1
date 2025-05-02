from abc import ABC, abstractmethod
from enum import Enum
from .atividade import Atividade, Trabalho, Prova, Aula_de_Campo, Apresentacao, TipoAtividade

class Disciplina(ABC):
    def __init__(self, nome, carga_horaria, semestre_id, codigo, observacao = None, id = None):
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.semestre_id = semestre_id
        self.atividades = []
        self.codigo = codigo
        self.observacao = observacao
        self.id = id

    def adicionar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO disciplina (nome, carga_horaria, semestre_id, codigo, observacao) VALUES (?, ?, ?, ?, ?)", (self.nome, self.carga_horaria, self.semestre_id, self.codigo, self.observacao))
        conexao.commit()
        self.id = cursor.lastrowid
    
    def editar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("UPDATE disciplina SET nome = ?, carga_horaria = ?, semestre_id = ?, observacao = ? WHERE id = ?", (self.nome, self.carga_horaria, self.semestre_id, self.observacao, self.id))
        conexao.commit()
    
    def deletar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM disciplina WHERE id = ?", (self.id,))
        conexao.commit()
    
    def adicionar_atividade(self, atividade):
        self.atividades.append(atividade)
    
    def carregar_atividades(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM atividade WHERE disciplina_id = ?", (self.id,))
        atividades = cursor.fetchall()
        print(atividades)
        for atividade in atividades:
            if atividade[6] == TipoAtividade.TRABALHO.value:
                self.atividades.append(Trabalho(atividade[1], atividade[2], atividade[3], atividade[5], atividade[6], atividade[7]))
            elif atividade[6] == TipoAtividade.PROVA.value:
                self.atividades.append(Prova(atividade[1], atividade[2], atividade[3], atividade[5], atividade[6], atividade[7]))
            elif atividade[6] == TipoAtividade.CAMPO.value:
                self.atividades.append(Aula_de_Campo(atividade[1], atividade[2], atividade[3], atividade[7]))
            elif atividade[6] == TipoAtividade.APRESENTACAO.value:
                self.atividades.append(Apresentacao(atividade[1], atividade[2], atividade[3], atividade[5], atividade[6], atividade[7]))
        return self.atividades
    
    def listar_atividades(self):
        for atividade in self.atividades:
            print(f"Atividade: {atividade.nome}, Data: {atividade.data}, Nota Total: {atividade.nota_total}, Observação: {atividade.observacao}")   
    
    