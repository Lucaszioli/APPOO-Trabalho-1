from app.models.disciplinas import Disciplina
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.semestre import Semestre  # Type hinting to avoid circular import

class SemestreService:
    @staticmethod
    def adicionar_bd(semestre, conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO semestre (nome, data_inicio, data_fim) VALUES (?, ?, ?)", (semestre.nome, semestre.data_inicio, semestre.data_fim))
        conexao.commit()
        semestre.id = cursor.lastrowid
        print("Adicionado com sucesso!")

    @staticmethod
    def editar_bd(semestre, conexao):
        cursor = conexao.cursor()
        cursor.execute("UPDATE semestre SET nome = ?, data_inicio = ?, data_fim = ? WHERE id = ?", (semestre.nome, semestre.data_inicio, semestre.data_fim, semestre.id))
        conexao.commit()
    
    @staticmethod
    def deletar_bd(semestre, conexao):
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM semestre WHERE id = ?", (semestre.id,))
        conexao.commit()
    
    
    @staticmethod
    def listar_semestres(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM semestre")
        semestres = cursor.fetchall()
        return [Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3]) for row in semestres]
    
    @staticmethod
    def buscar_ultimo_semestre(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM semestre ORDER BY data_fim DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            return Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3])
        return None
    
    @staticmethod
    def carregar_disciplinas(semestre, conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM disciplina WHERE semestre_id = ?", (semestre.id,))
        disciplinas = cursor.fetchall()
        for disciplina in disciplinas:
            semestre.disciplinas.append(Disciplina(nome=disciplina[1], carga_horaria=disciplina[2], semestre_id=disciplina[3], codigo=disciplina[4], observacao=disciplina[5], id=disciplina[0]))
