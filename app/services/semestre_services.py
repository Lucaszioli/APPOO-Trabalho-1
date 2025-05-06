from app.models.disciplinas import Disciplina
from app.errors.nomeSemestre import NomeRepetidoError
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.semestre import Semestre 

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
        from app.models.semestre import Semestre
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
        semestre.disciplinas = []
        for disciplina in disciplinas:
            semestre.disciplinas.append(Disciplina(nome=disciplina[1], carga_horaria=disciplina[2], semestre_id=disciplina[3], codigo=disciplina[4], observacao=disciplina[5], id=disciplina[0]))
    @staticmethod
    def buscar_por_nome(nome, conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM semestre WHERE nome = ?", (nome,))
        semestre = cursor.fetchone()
        if semestre:
            raise NomeRepetidoError(nome)
            
    @staticmethod
    def criar(nome, data_inicio, data_fim, conexao):
        from app.models.semestre import Semestre
        SemestreService.buscar_por_nome(nome, conexao)
        semestre = Semestre(nome, data_inicio, data_fim)
        SemestreService.adicionar_bd(semestre, conexao)
        return semestre