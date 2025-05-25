from app.errors.notFound import DisciplinaNotFoundError

from app.models.atividade import TipoAtividadeEnum, Trabalho, Aula_de_Campo, Prova, Revisao
from app.models.disciplinas import Disciplina
from app.models.atividade import Atividade
from app.models.semestre import Semestre
from app.services.service_base import ServiceBase

class DisciplinaService(ServiceBase):
    def __init__(self, db_path="db.db"):
        super().__init__(db_path)

    def _adicionar_bd(self, disciplina:"Disciplina") -> "Disciplina":
        self.query = "INSERT INTO disciplina (nome, carga_horaria, semestre_id, codigo, observacao) VALUES (?, ?, ?, ?, ?)"
        self.params = (disciplina.nome, disciplina.carga_horaria, disciplina.semestre_id, disciplina.codigo, disciplina.observacao)
        disciplina.id = self._adicionar(self.query, self.params)
        return disciplina
    
    def buscar_por_id(self, id:str) -> "Disciplina":
        self.query = "SELECT * FROM disciplina WHERE id = ?"
        self.params = (id,)
        self.disciplina = self._buscar(self.query, self.params)
        return Disciplina(id=self.disciplina[0], nome=self.disciplina[1], carga_horaria=self.disciplina[2], semestre_id=self.disciplina[3], codigo=self.disciplina[4], observacao=self.disciplina[5])

    def editar_bd(self,disciplina:"Disciplina") -> "Disciplina":
        self.disciplinaExistente = self.buscar_por_id(disciplina.id)
        if not self.disciplinaExistente:
            raise DisciplinaNotFoundError()
        self.query = "UPDATE disciplina SET nome = ?, carga_horaria = ?, semestre_id = ?, codigo = ?, observacao = ? WHERE id = ?"
        self.params = (disciplina.nome, disciplina.carga_horaria, disciplina.semestre_id, disciplina.codigo, disciplina.observacao, disciplina.id)
        self._editar(self.query, self.params)
        return disciplina
    
    def deletar(self, disciplina:"Disciplina") -> int:
        self.disciplinaExistente = self.buscar_por_id(disciplina.id)
        if not self.disciplinaExistente:
            raise DisciplinaNotFoundError()
        self.query = "DELETE FROM disciplina WHERE id = ?"
        self.params = (disciplina.id,)
        self.rows = self._deletar(self.query, self.params)
        del disciplina
        return self.rows

    def carregar_atividades(self, disciplina:"Disciplina") -> list[Atividade]:
        self.query = "SELECT * FROM atividade WHERE disciplina_id = ?"
        self.params = (disciplina.id,)
        self.atividades = self._buscar(self.query, self.params)
        for atividade in self.atividades:
            if atividade[6] == TipoAtividadeEnum().TRABALHO.value:
                disciplina.adicionar_atividade(Trabalho(atividade[1], atividade[2], atividade[3], atividade[5], atividade[6], atividade[7]))
            elif atividade[6] == TipoAtividadeEnum().PROVA.value:
                disciplina.adicionar_atividade(Prova(atividade[1], atividade[2], atividade[3], atividade[5], atividade[6], atividade[7]))
            elif atividade[6] == TipoAtividadeEnum().CAMPO.value:
                disciplina.adicionar_atividade(Aula_de_Campo(atividade[1], atividade[2], atividade[3], atividade[7]))
            elif atividade[6] == TipoAtividadeEnum().REVISAO.value:
                disciplina.adicionar_atividade(Revisao(atividade[1], atividade[2], atividade[3], atividade[5], atividade[6], atividade[7]))
        return disciplina.atividades
    
    def criar_disciplina(self, nome:str, carga_horaria:int, codigo:str, semestre:"Semestre", observacao:str = None):
        self.disciplina = Disciplina(nome, carga_horaria, semestre.id, codigo, observacao)
        self._adicionar_bd(self.disciplina)
        semestre.adicionar_disciplina(self.disciplina)
        return self.disciplina
    

    def listar_por_semestre(self,semestre:"Semestre"):
        self.query = "SELECT * FROM disciplina WHERE semestre_id = ?"
        self.params = (semestre.id,)
        self.disciplinas = self._buscar_varios(self.query, self.params)
        if not self.disciplinas:
            return []
        return [Disciplina(id=row[0], nome=row[1], carga_horaria=row[2], semestre_id=row[3], codigo=row[4], observacao=row[5]) for row in self.disciplinas]
    
    def listar(self) -> list["Disciplina"]:
        self.query = "SELECT * FROM disciplina"
        self.params = ()
        disciplinas = self._buscar_varios(self.query, self.params)
        if not disciplinas:
            return []
        return [Disciplina(id=row[0], nome=row[1], carga_horaria=row[2], semestre_id=row[3], codigo=row[4], observacao=row[5]) for row in self.disciplinas]
    

        