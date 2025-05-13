from sqlite3 import Connection
from app.models.disciplinas import Disciplina
from app.errors.nomeSemestre import NomeRepetidoError
from app.errors.notFound import SemestreNotFoundError
from typing import TYPE_CHECKING, Optional
from app.utils.database import Database

if TYPE_CHECKING:
    from app.models.semestre import Semestre 

class SemestreService(Database):

    @staticmethod
    def __adicionar_bd(semestre:"Semestre", conexao:Connection) -> "Semestre":
        query = "INSERT INTO semestre (nome, data_inicio, data_fim) VALUES (?, ?, ?)"
        params = (semestre.nome, semestre.data_inicio, semestre.data_fim)
        semestre.id = Database._adicionar(query,params,conexao)
        return semestre

    @staticmethod
    def editar_bd(semestre:"Semestre", conexao:Connection) -> "Semestre":
        semestreExistente = SemestreService.buscar_por_id(semestre.id, conexao)
        if not semestreExistente:
            raise SemestreNotFoundError()
        
        query = "UPDATE semestre SET nome = ?, data_inicio = ?, data_fim = ? WHERE id = ?"
        params = (semestre.nome, semestre.data_inicio, semestre.data_fim, semestre.id)
        Database._editar(query, params, conexao)
        return semestre
    
    @staticmethod
    def buscar_por_id(id:str, conexao:Connection) -> Optional["Semestre"]:
        from app.models.semestre import Semestre
        query = "SELECT * FROM semestre WHERE id = ?"
        params = (id,)
        row = Database._buscar_um(query, params, conexao)
        if row:
            return Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3])
        return None
    
    @staticmethod
    def deletar_semestre(semestre:"Semestre", conexao:Connection) -> int:
        semestre = SemestreService.buscar_por_id(semestre.id, conexao)
        if not semestre:
            raise SemestreNotFoundError()
        query = "DELETE FROM semestre WHERE id = ?"
        params = (semestre.id,)
        rows = Database._deletar(query, params, conexao)
        del semestre
        return rows

    
    @staticmethod
    def listar_semestres(conexao:Connection) -> list["Semestre"]:
        from app.models.semestre import Semestre
        query = "SELECT * FROM semestre"
        params = ()
        semestres = Database._buscar_varios(query, params, conexao)
        if not semestres:
            return []
        return [Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3]) for row in semestres]
    
    @staticmethod
    def buscar_ultimo_semestre(conexao:Connection) -> Optional["Semestre"]:
        query = "SELECT * FROM semestre ORDER BY id DESC LIMIT 1"
        params = ()
        semestre = Database._buscar_um(query, params, conexao)
        if semestre:
            return Semestre(id=semestre[0], nome=semestre[1], data_inicio=semestre[2], data_fim=semestre[3])
        return None
    
    
    def carregar_disciplinas(self, semestre:"Semestre", conexao:Connection) -> list["Disciplina"]:
        from app.models.disciplinas import Disciplina
        query = "SELECT * FROM disciplina WHERE semestre_id = ?"
        params = (semestre.id,)
        disciplinas = self._buscar_varios(query, params, conexao)
        for row in disciplinas:
            disciplina = Disciplina(id=row[0], nome=row[1], carga_horaria=row[2], semestre_id=row[3], codigo=row[4], observacao=row[5])
            semestre.adicionar_disciplina(disciplina)
        return semestre.disciplinas

    @staticmethod
    def buscar_por_nome(nome:str, conexao:Connection) -> Optional["Semestre"]:
        from app.models.semestre import Semestre
        query = "SELECT * FROM semestre WHERE nome = ?"
        params = (nome,)
        row = Database._buscar_um(query, params, conexao)
        if row:
            return Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3])
        return None
            
    @staticmethod
    def criar(nome:str, data_inicio:str, data_fim:str, conexao:Connection) -> "Semestre":
        from app.models.semestre import Semestre
        semestre = SemestreService.buscar_por_nome(nome, conexao)
        if semestre:
            raise NomeRepetidoError(nome)
        semestre = Semestre(nome, data_inicio, data_fim)
        SemestreService.__adicionar_bd(semestre, conexao)
        return semestre
    