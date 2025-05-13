from app.models.disciplinas import Disciplina
from app.errors.nomeSemestre import NomeRepetidoError
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.semestre import Semestre 
from app.utils.database import Database
class SemestreService(Database):
    def __init__(self):
        pass

    def __adicionar_bd(self,semestre, conexao):
        query = "INSERT INTO semestre (nome, data_inicio, data_fim) VALUES (?, ?, ?)"
        params = (semestre.nome, semestre.data_inicio, semestre.data_fim)
        semestre.id = self._adicionar(query,params,conexao)
        return semestre

    def editar_bd(self, semestre, conexao):
        query = "UPDATE semestre SET nome = ?, data_inicio = ?, data_fim = ? WHERE id = ?"
        params = (semestre.nome, semestre.data_inicio, semestre.data_fim, semestre.id)
        self._editar(query, params, conexao)
        return semestre
    
    def buscar_por_id(self, id, conexao):
        from app.models.semestre import Semestre
        query = "SELECT * FROM semestre WHERE id = ?"
        params = (id,)
        row = self._buscar_um(query, params, conexao)
        if row:
            return Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3])
        return None
    
    
    def deletar_bd(self,semestre, conexao):
        query = "DELETE FROM semestre WHERE id = ?"
        params = (semestre.id,)
        self._deletar(query, params, conexao)
        return semestre
    
    
    def listar_semestres(self,conexao):
        from app.models.semestre import Semestre
        query = "SELECT * FROM semestre"
        params = ()
        semestres = self._buscar_varios(query, params, conexao)
        if not semestres:
            return []
        return [Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3]) for row in semestres]
    
    @staticmethod
    def buscar_ultimo_semestre(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM semestre ORDER BY data_fim DESC LIMIT 1")
        semestre = cursor.fetchone()
        if semestre:
            return Semestre(id=semestre[0], nome=semestre[1], data_inicio=semestre[2], data_fim=semestre[3])
        return None
    
    
    def carregar_disciplinas(self, semestre, conexao):
        from app.models.disciplinas import Disciplina
        query = "SELECT * FROM disciplina WHERE semestre_id = ?"
        params = (semestre.id,)
        disciplinas = self._buscar_varios(query, params, conexao)
        for row in disciplinas:
            disciplina = Disciplina(id=row[0], nome=row[1], carga_horaria=row[2], semestre_id=row[3], codigo=row[4], observacao=row[5])
            semestre.adicionar_disciplina(disciplina)
        return semestre.disciplinas

    def buscar_por_nome(self,nome, conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM semestre WHERE nome = ?", (nome,))
        semestre = cursor.fetchone()
        return semestre
            
    @staticmethod
    def criar(nome, data_inicio, data_fim, conexao):
        from app.models.semestre import Semestre
        service = SemestreService()
        semestre = service.buscar_por_nome(nome, conexao)
        if semestre:
            raise NomeRepetidoError(nome)
        semestre = Semestre(nome, data_inicio, data_fim)
        service.__adicionar_bd(semestre, conexao)
        return semestre
    