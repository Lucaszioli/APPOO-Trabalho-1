from app.models.disciplinas import Disciplina
from app.errors.nomeSemestre import NomeRepetidoError
from app.errors.notFound import SemestreNotFoundError
from typing import TYPE_CHECKING, Optional
from app.services.disciplinas_services import DisciplinaService
from app.services.service_base import ServiceBase
from app.models.semestre import Semestre 

class SemestreService(ServiceBase):

    def __init__(self, db_path="db.db"):
        super().__init__(db_path)


    def _adicionar_bd(self, semestre:"Semestre") -> "Semestre":
        self.query = "INSERT INTO semestre (nome, data_inicio, data_fim) VALUES (?, ?, ?)"
        self.params = (semestre.nome, semestre.data_inicio, semestre.data_fim)
        semestre.id = self._adicionar(self.query,self.params)
        return semestre

    def buscar_por_id(self,id:str) -> Optional["Semestre"]:
        self.query = "SELECT * FROM semestre WHERE id = ?"
        self.params = (id,)
        row = self._buscar_um(self.query, self.params)
        if row:
            return Semestre(id=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3])
        return None
    
    def editar_bd(self, semestre:"Semestre") -> "Semestre":
        self.semestreExistente = self.buscar_por_id(semestre.id)
        if not self.semestreExistente:
            raise SemestreNotFoundError()
        
        self.query = "UPDATE semestre SET nome = ?, data_inicio = ?, data_fim = ? WHERE id = ?"
        self.params = (semestre.nome, semestre.data_inicio, semestre.data_fim, semestre.id)
        self._editar(self.query, self.params)
        return semestre
    
    
    def deletar(self, semestre:"Semestre") -> int:
        semestre = self.buscar_por_id(semestre.id)
        if not semestre:
            raise SemestreNotFoundError()
        self.query = "DELETE FROM semestre WHERE id = ?"
        self.params = (semestre.id,)
        self.rows = self._deletar(self.query, self.params)
        del semestre
        return self.rows

    
    def listar(self) -> list["Semestre"]:
        self.query = "SELECT * FROM semestre"
        self.params = ()
        self.semestres = self._buscar_varios(self.query, self.params)
        if not self.semestres:
            return []
        semestres = [Semestre(
            id=row[0], 
            nome=row[1], 
            data_inicio=row[2], 
            data_fim=row[3]
        ) for row in self.semestres]
        for semestre in semestres:
            semestre.nsg = self.calcular_nsg(semestre)
        return semestres
    

    def buscar_ultimo_semestre(self) -> Optional["Semestre"]:
        """Busca o último semestre cadastrado no banco de dados."""

        self.query = "SELECT * FROM semestre ORDER BY id DESC LIMIT 1"
        self.params = ()
        self.semestre = self._buscar_um(self.query, self.params)
        if self.semestre:
            return Semestre(
                id=self.semestre[0], 
                nome=self.semestre[1], 
                data_inicio=self.semestre[2], 
                data_fim=self.semestre[3]
            )
        return None
    
    
    def carregar_disciplinas(self, semestre:"Semestre") -> list["Disciplina"]:
        """Carrega as disciplinas associadas a um semestre."""

        semestre.disciplinas = []
        self.query = "SELECT * FROM disciplina WHERE semestre_id = ?"
        self.params = (semestre.id,)
        self.disciplinas = self._buscar_varios(self.query, self.params)
        for row in self.disciplinas:
            disciplina = Disciplina(
                id=row[0], 
                nome=row[1], 
                codigo=row[2], 
                carga_horaria=row[3], 
                semestre_id=row[4], 
                observacao=row[5]
            )
            semestre.adicionar_disciplina(disciplina)
        return semestre.disciplinas

    def buscar_por_nome(self,nome:str) -> Optional["Semestre"]:
        """Busca um semestre pelo nome."""

        self.query = "SELECT * FROM semestre WHERE nome = ?"
        self.params = (nome,)
        row = self._buscar_um(self.query, self.params)
        if row:
            return Semestre(
                id=row[0], 
                nome=row[1], 
                data_inicio=row[2], 
                data_fim=row[3]
            )
        return None
            
    def criar_semestre(self, nome:str, data_inicio:str, data_fim:str) -> "Semestre":
        """Cria um novo semestre e o adiciona ao banco de dados."""

        self.semestreExistente = self.buscar_por_nome(nome)
        if self.semestreExistente:
            raise NomeRepetidoError(nome)
        semestre = Semestre(nome, data_inicio, data_fim)
        self._adicionar_bd(semestre)
        return semestre
    
    def calcular_nsg(self, semestre:"Semestre") -> float:
        """Calcula o NSG (Nota Semestral Geral) de um semestre."""
        
        from app.services.disciplinas_services import DisciplinaService
        self.carregar_disciplinas(semestre)
        if not semestre.disciplinas:
            return 0.0
        total_nota = 0.0
        total_creditos = 0
        disciplina_service = DisciplinaService()
        for disciplina in semestre.disciplinas:
            nota_final = disciplina_service.pegar_nota_total(disciplina)
            if nota_final:
                total_nota += nota_final * disciplina.carga_horaria
                total_creditos += disciplina.carga_horaria
        if total_creditos == 0:
            return 0.0
        return total_nota / total_creditos if total_creditos > 0 else 0.0