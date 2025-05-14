from sqlite3 import Connection
from app.models.disciplinas import Disciplina
from app.errors.nomeSemestre import NomeRepetidoError
from app.errors.notFound import SemestreNotFoundError
from typing import TYPE_CHECKING, Optional
from app.utils.database import Database

if TYPE_CHECKING:
    from app.models.semestre import Semestre 

class SemestreService(Database):

    def __init__(self, db_path="db.db"):
        super().__init__(db_path)


    def __adicionar_bd(self, semestre:"Semestre") -> "Semestre":
        self.query = "INSERT INTO semestre (nome, data_inicio, data_fim) VALUES (?, ?, ?)"
        self.params = (semestre.nome, semestre.data_inicio, semestre.data_fim)
        semestre.id = self._adicionar(self.query,self.params)
        return semestre

    def editar_bd(self, semestre:"Semestre") -> "Semestre":
        self.semestreExistente = self.buscar_por_id(semestre.id)
        if not self.semestreExistente:
            raise SemestreNotFoundError()
        
        self.query = "UPDATE semestre SET nome = ?, data_inicio = ?, data_fim = ? WHERE id = ?"
        self.params = (semestre.nome, semestre.data_inicio, semestre.data_fim, semestre.id)
        self._editar(self.query, self.params)
        return semestre
    
    def buscar_por_id(self,id:str) -> Optional["Semestre"]:
        from app.models.semestre import Semestre
        self.query = "SELECT * FROM semestre WHERE id = ?"
        self.params = (id,)
        row = self._buscar_um(self.query, self.params)
        if row:
            return Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3])
        return None
    
    def deletar_semestre(self, semestre:"Semestre") -> int:
        semestre = self.buscar_por_id(semestre.id)
        if not semestre:
            raise SemestreNotFoundError()
        self.query = "DELETE FROM semestre WHERE id = ?"
        self.params = (semestre.id,)
        rows = self._deletar(self.query, self.params)
        del semestre
        return rows

    
    def listar_semestres(self) -> list["Semestre"]:
        from app.models.semestre import Semestre
        self.query = "SELECT * FROM semestre"
        self.params = ()
        semestres = self._buscar_varios(self.query, self.params)
        if not semestres:
            return []
        return [Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3]) for row in semestres]
    

    def buscar_ultimo_semestre(self) -> Optional["Semestre"]:
        self.query = "SELECT * FROM semestre ORDER BY id DESC LIMIT 1"
        self.params = ()
        semestre = self._buscar_um(self.query, self.params)
        if semestre:
            return Semestre(id=semestre[0], nome=semestre[1], data_inicio=semestre[2], data_fim=semestre[3])
        return None
    
    
    def carregar_disciplinas(self, semestre:"Semestre") -> list["Disciplina"]:
        from app.models.disciplinas import Disciplina
        self.query = "SELECT * FROM disciplina WHERE semestre_id = ?"
        self.params = (semestre.id,)
        disciplinas = self._buscar_varios(self.query, self.params)
        for row in disciplinas:
            disciplina = Disciplina(id=row[0], nome=row[1], carga_horaria=row[2], semestre_id=row[3], codigo=row[4], observacao=row[5])
            semestre.adicionar_disciplina(disciplina)
        return semestre.disciplinas

    def buscar_por_nome(self,nome:str) -> Optional["Semestre"]:
        from app.models.semestre import Semestre
        self.query = "SELECT * FROM semestre WHERE nome = ?"
        self.params = (nome,)
        row = self._buscar_um(self.query, self.params)
        if row:
            return Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3])
        return None
            
    def criar_semestre(self, nome:str, data_inicio:str, data_fim:str) -> "Semestre":
        from app.models.semestre import Semestre
        self.semestreExistente = self.buscar_por_nome(nome)
        if self.semestreExistente:
            raise NomeRepetidoError(nome)
        semestre = Semestre(nome, data_inicio, data_fim)
        self.__adicionar_bd(semestre)
        return semestre
    