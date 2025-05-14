from abc import ABC, abstractmethod
from app.models.atividade import Atividade

class AtividadeService(ABC):
    @staticmethod
    def listar_atividades(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM atividades")
        atividades  = cursor.fetchall()
        return[Atividade()]


class TrabalhoService:
    @staticmethod
    def adicionar_bd(atividade,conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO atividade (nome, data, disciplina_id, tipo, nota_total, nota, observacao) VALUES (?, ?, ?, ?, ?, ?, ?)", (atividade.nome, atividade.data, atividade.disciplina_id, atividade.tipo.value, atividade.nota_total, atividade.nota, atividade.observacao))
        conexao.commit()
        atividade.id = cursor.lastrowid

    @staticmethod
    def editar_bd(atividade, conexao):
        cursor = conexao.cursor()
        cursor.execute("UPDATE atividade SET nome = ?, data = ?, disciplina_id = ?, tipo = ?, nota_total = ?, nota = ?, observacao = ? WHERE id = ?", (atividade.nome, atividade.data, atividade.disciplina_id, atividade.tipo.value, atividade.nota_total, atividade.nota, atividade.observacao, atividade.id))
        conexao.commit()

    @staticmethod 
    def deletar_bd(atividade, conexao):
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM atividade WHERE id = ?", (atividade.id))
        conexao.commit()

