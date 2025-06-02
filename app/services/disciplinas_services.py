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
        self.disciplina = self._buscar_um(self.query, self.params)
        return Disciplina(id=self.disciplina[0], nome=self.disciplina[1], carga_horaria=self.disciplina[3], semestre_id=self.disciplina[4], codigo=self.disciplina[2], observacao=self.disciplina[5])



    def editar_bd(self,disciplina:"Disciplina") -> "Disciplina":
        self.disciplinaExistente = self.buscar_por_id(disciplina.id)
        if not self.disciplinaExistente:
            raise DisciplinaNotFoundError()
        self.query = "UPDATE disciplina SET nome = ?, carga_horaria = ?, codigo = ?, observacao = ? WHERE id = ?"
        self.params = (disciplina.nome, disciplina.carga_horaria, disciplina.codigo, disciplina.observacao, disciplina.id)
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
        self.atividades = self._buscar_varios(self.query, self.params)
        for atividade in self.atividades:
            if atividade[6] == TipoAtividadeEnum().TRABALHO:
                disciplina.adicionar_atividade(Trabalho(
                    nome=atividade[1],
                    data=atividade[2],
                    disciplina_id=disciplina.id,
                    nota=atividade[3],
                    nota_total=atividade[4],
                    observacao=atividade[5],
                    data_apresentacao=atividade[9],
                    id=atividade[0],
                ))
            elif atividade[6] == TipoAtividadeEnum().PROVA:
                disciplina.adicionar_atividade(Prova(
                    nome=atividade[1],
                    data=atividade[2],
                    disciplina_id=disciplina.id,
                    nota=atividade[3],
                    nota_total=atividade[4],
                    observacao=atividade[5],
                    id=atividade[0]
                ))
            elif atividade[6] == TipoAtividadeEnum().CAMPO:
                disciplina.adicionar_atividade(Aula_de_Campo(
                    nome=atividade[1],
                    data=atividade[2],
                    disciplina_id=disciplina.id,
                    id=atividade[0],
                    observacao=atividade[7] if len(atividade) > 7 else None
                ))
            elif atividade[6] == TipoAtividadeEnum().REVISAO:
                disciplina.adicionar_atividade(Revisao(
                    nome=atividade[1],
                    data=atividade[2],
                    disciplina_id=disciplina.id,
                    observacao=atividade[5],
                    id=atividade[0]
                ))
        return disciplina.atividades
    
    def criar_disciplina(self,
        nome:str, 
        carga_horaria:int, 
        codigo:str, 
        semestre:"Semestre", 
        observacao:str = None
    ):
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
        return [Disciplina(
            id=row[0], 
            nome=row[1], 
            codigo=row[2], 
            carga_horaria=row[3], 
            semestre_id=row[4], 
            observacao=row[5]
        ) for row in self.disciplinas]
    
    def listar(self) -> list["Disciplina"]:
        self.query = "SELECT * FROM disciplina"
        self.params = ()
        disciplinas = self._buscar_varios(self.query, self.params)
        if not disciplinas:
            return []
        return [Disciplina(
            id=row[0], 
            nome=row[1], 
            codigo=row[2], 
            carga_horaria=row[3], 
            semestre_id=row[4], 
            observacao=row[5]
        ) for row in self.disciplinas]

    def pegar_nota_total(self, disciplina: "Disciplina") -> float:
        """
        Calcula a nota final da disciplina com base nas atividades cadastradas.
        Retorna 0.0 se não houver atividades ou notas.
        """
        self.carregar_atividades(disciplina)
        if not hasattr(disciplina, 'atividades') or not disciplina.atividades:
            return 0.0
        total = 0.0
        peso_total = 0.0
        for atividade in disciplina.atividades:
            print(atividade.__dict__)
            if hasattr(atividade, 'nota') and hasattr(atividade, 'nota_total') and atividade.nota_total and atividade.nota:
                total += (atividade.nota / atividade.nota_total) * 100
                peso_total += 1
        if peso_total == 0:
            return 0.0
        return total / peso_total


