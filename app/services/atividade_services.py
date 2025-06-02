from abc import ABC, abstractmethod
from app.errors.incorrectDate import incorrectDate
from app.utils.database import Database
from app.models.disciplinas import Disciplina
from app.models.atividade import Atividade, Trabalho, Prova, Aula_de_Campo, Revisao,TipoAtividadeEnum
from typing import Optional
from app.errors.notFound import AtividadeNotFoundError, DisciplinaNotFoundError, SemestreNotFoundError
from app.models.semestre import Semestre
from app.services.semestre_services import SemestreService
from app.services.disciplinas_services import DisciplinaService
from datetime import datetime, timedelta
class AtividadeService(ABC, Database):

    def __init__(self, db_path="db.db"):
        super().__init__(db_path)

    def _adicionar_bd(self, atividade:"Atividade") -> Atividade:
        self.query = "INSERT INTO atividade (nome, data, disciplina_id, tipo, nota_total, nota, observacao, lugar, data_apresentacao, materia, progresso) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.params = (
            atividade.nome, 
            atividade.data,
            atividade.disciplina_id, 
            atividade.tipo, 
            getattr(atividade,"nota_total", None), 
            getattr(atividade,"nota", None), 
            getattr(atividade,"observacao", None), 
            getattr(atividade,"lugar", None),
            getattr(atividade,"data_apresentacao", None),
            getattr(atividade, "materia", None),
            getattr(atividade, "progresso", 'Não começou')
        )
        atividade.id = self._adicionar(self.query, self.params)
        return atividade
    
    def listar(self) -> list[Atividade]:
        self.query = "SELECT * FROM atividade"
        self.params = ()
        atividades = self._buscar_varios(self.query, self.params)
        if not atividades:
            return []
        result = []
        for atividade in atividades:
            progresso = atividade[11] if len(atividade) > 11 else 'Não começou'
            if atividade[6] == TipoAtividadeEnum().TRABALHO:
                result.append(Trabalho(id=atividade[0], nome=atividade[1], data=atividade[2], nota=atividade[3], nota_total=atividade[4], disciplina_id=atividade[5], observacao=atividade[7], data_apresentacao=atividade[9], progresso=progresso))
            elif atividade[6] == TipoAtividadeEnum().PROVA:
                result.append(Prova(id=atividade[0], nome=atividade[1], data=atividade[2], nota=atividade[3], nota_total=atividade[4], disciplina_id=atividade[5], observacao=atividade[7], progresso=progresso))
            elif atividade[6] == TipoAtividadeEnum().CAMPO:
                result.append(Aula_de_Campo(id=atividade[0], nome=atividade[1], data=atividade[2], disciplina_id=atividade[5], observacao=atividade[7], lugar=atividade[8], progresso=progresso))
            elif atividade[6] == TipoAtividadeEnum().REVISAO:
                result.append(Revisao(id=atividade[0], nome=atividade[1], data=atividade[2], disciplina_id=atividade[5], observacao=atividade[7], materia=atividade[10], progresso=progresso))
            else:   
                raise ValueError("Tipo de atividade inválido")
        return result
    
    def listar_por_disciplina(self, disciplina:"Disciplina") -> list[Atividade]:
        """Lista todas as atividades de uma disciplina específica ordenadas por data."""

        self.query = "SELECT * FROM atividade WHERE disciplina_id = ? ORDER BY data ASC"
        self.params = (disciplina.id,)
        atividades = self._buscar_varios(self.query, self.params)
        if not atividades:
            return []
        result = []
        for atividade in atividades:
            progresso = atividade[11] if len(atividade) > 11 else 'Não começou'
            if atividade[6] == TipoAtividadeEnum().TRABALHO:
                result.append(Trabalho(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    nota=atividade[3], 
                    nota_total=atividade[4], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7], 
                    data_apresentacao=atividade[9],
                    progresso=progresso
                ))
                if atividade[9] : # Se houver data de apresentação, adiciona uma instância separada para a apresentação
                    result.append(Trabalho(
                        id=atividade[0], 
                        nome=atividade[1]+" (apresentação)", 
                        nota=None, 
                        nota_total=None,
                        disciplina_id=atividade[5], 
                        observacao="Apresentação do trabalho",
                        data=atividade[9], 
                        progresso=atividade[11]
                    ))
            elif atividade[6] == TipoAtividadeEnum().PROVA:
                result.append(Prova(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    nota=atividade[3], 
                    nota_total=atividade[4], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7],
                    progresso=progresso
                ))
            elif atividade[6] == TipoAtividadeEnum().CAMPO:
                result.append(Aula_de_Campo(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7], 
                    lugar=atividade[8],
                    progresso=progresso
                ))
            elif atividade[6] == TipoAtividadeEnum().REVISAO:
                result.append(Revisao(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7], 
                    materia=atividade[10],
                    progresso=progresso
                ))
            else:   
                raise ValueError("Tipo de atividade inválido")
        result.sort(key = lambda atv: datetime.strptime(atv.data, "%d/%m/%Y"))
        return result

    
    def buscar_por_id(self, id:str) -> Optional[Atividade]:
        self.query = "SELECT * FROM atividade WHERE id = ?"
        self.params = (id,)
        atividade = self._buscar_um(self.query, self.params)
        if atividade:
            progresso = atividade[11] if len(atividade) > 11 else 'Não começou'
            if atividade[6] == TipoAtividadeEnum().TRABALHO:
                return Trabalho(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    nota=atividade[3],
                    nota_total=atividade[4], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7], 
                    data_apresentacao=atividade[9],
                    progresso=progresso
                )
            elif atividade[6] == TipoAtividadeEnum().PROVA:
                return Prova(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    nota=atividade[3], 
                    nota_total=atividade[4],
                    disciplina_id=atividade[5], 
                    observacao=atividade[7],
                    progresso=progresso
                )
            elif atividade[6] == TipoAtividadeEnum().CAMPO:
                return Aula_de_Campo(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    disciplina_id=atividade[5],
                    observacao=atividade[7], 
                    lugar=atividade[8],
                    progresso=progresso
                )
            elif atividade[6] == TipoAtividadeEnum().REVISAO:
                return Revisao(id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7], 
                    materia=atividade[10],
                    progresso=progresso
                )
            else:   
                raise ValueError("Tipo de atividade inválido")
        return None
    
    def editar_bd(self, atividade:"Atividade") -> "Atividade":
        self.atividadeExistente = self.buscar_por_id(atividade.id)
        if not self.atividadeExistente:
            raise AtividadeNotFoundError()
        self.query = "UPDATE atividade SET nome = ?, data = ?, disciplina_id = ?, tipo = ?, nota_total = ?, nota = ?, observacao = ?, lugar = ?, data_apresentacao = ?, progresso = ? WHERE id = ?"
        self.params = (atividade.nome, atividade.data, atividade.disciplina_id, atividade.tipo, atividade.nota_total, atividade.nota, atividade.observacao, atividade.lugar, atividade.data_apresentacao, atividade.progresso, atividade.id)
        self._editar(self.query, self.params)
        return atividade
    
    def deletar(self, atividade:"Atividade") -> Atividade:
        self.atividadeExistente = self.buscar_por_id(atividade.id)
        if not self.atividadeExistente:
            raise AtividadeNotFoundError()
        self.query = "DELETE FROM atividade WHERE id = ?"
        self.params = (atividade.id,)
        self.rows = self._deletar(self.query, self.params)
        del atividade
        return self.rows
    
    def criar_atividade(self,
        nome:str, 
        data:str, 
        disciplina:"Disciplina",
        tipo:"TipoAtividadeEnum", 
        nota_total:float=None, 
        nota:float = None, 
        observacao:str = None, 
        lugar:str = None, 
        data_apresentacao:str = None, 
        materia=None,
        progresso:str = 'Não começou'
        ) -> Atividade:
        self.semestreExistente = SemestreService(self._db_path).buscar_por_id(disciplina.semestre_id)
        """Cria uma nova atividade e a adiciona ao banco de dados e à disciplina associada."""

        if not self.semestreExistente:
            raise SemestreNotFoundError()
        self.disciplinaExistente = DisciplinaService(self._db_path).buscar_por_id(disciplina.id)
        if not self.disciplinaExistente:
            raise DisciplinaNotFoundError()
        
        inicio_s = datetime.strptime(self.semestreExistente.data_inicio, "%d/%m/%Y")
        fim_s = datetime.strptime(self.semestreExistente.data_fim, "%d/%m/%Y")
        data_t = datetime.strptime(data, "%d/%m/%Y")
        if data_t < inicio_s or data_t > fim_s:
            raise incorrectDate(data_t, "Data da atividade fora do período do semestre")

        if tipo == TipoAtividadeEnum().TRABALHO:
            if data_apresentacao:
                data_apresentacao_t = datetime.strptime(data_apresentacao, "%d/%m/%Y")
                print(data_apresentacao_t, data_t)
                if data_apresentacao_t < data_t :
                    raise incorrectDate(data_apresentacao_t, "Data de apresentação não pode ser anterior à data do trabalho")
                if (data_apresentacao_t < inicio_s or data_apresentacao_t > fim_s):
                    raise incorrectDate(data_apresentacao_t, "Data de apresentação fora do período do semestre")
            atividade = Trabalho(nome, data, disciplina.id, nota_total=nota_total, nota=nota, observacao=observacao, data_apresentacao=data_apresentacao, progresso=progresso)
        elif tipo == TipoAtividadeEnum().PROVA:
            atividade = Prova(nome, data, disciplina.id, nota_total, nota=nota, observacao=observacao, progresso=progresso)
        elif tipo == TipoAtividadeEnum().CAMPO:
            atividade = Aula_de_Campo(nome, data, disciplina.id, lugar=lugar, observacao=observacao, progresso=progresso)
        elif tipo == TipoAtividadeEnum().REVISAO:
            atividade = Revisao(nome, data, disciplina.id, observacao=observacao, materia=materia, progresso=progresso)
        else:
            raise ValueError("Tipo de atividade inválido")
        
        self._adicionar_bd(atividade)
        disciplina.adicionar_atividade(atividade)
        return atividade
    
    def listar_por_semestre(self, semestre:"Semestre") -> list[Atividade]:
        """Lista todas as atividades de um semestre específico ordenadas por data."""

        self.query = (
            "SELECT * FROM atividade "
            "WHERE disciplina_id IN (SELECT id FROM disciplina WHERE semestre_id = ?) "
            "ORDER BY data ASC"
        )
        self.params = (semestre.id,)

        self.semestreExistente = SemestreService(self._db_path).buscar_por_id(semestre.id)
        if not self.semestreExistente:
            raise SemestreNotFoundError()
        
        atividades = self._buscar_varios(self.query, self.params)
        if not atividades:
            return []
        
        result = []
        for atividade in atividades:
            if atividade[6] == TipoAtividadeEnum().TRABALHO:
                result.append(Trabalho(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    nota=atividade[3], 
                    nota_total=atividade[4], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7], 
                    data_apresentacao=atividade[9]
                ))
                if atividade[9] : # Se houver data de apresentação, adiciona uma instância separada para a apresentação
                    result.append(Trabalho(
                        id=atividade[0], 
                        nome=atividade[1]+" (apresentação)", 
                        nota=None, 
                        nota_total=None,
                        disciplina_id=atividade[5], 
                        observacao="Apresentação do trabalho",
                        data=atividade[9], 
                        progresso=atividade[11]
                    ))
            elif atividade[6] == TipoAtividadeEnum().PROVA:
                result.append(Prova(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    nota=atividade[3], 
                    nota_total=atividade[4], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7]
                ))
            elif atividade[6] == TipoAtividadeEnum().CAMPO:
                result.append(Aula_de_Campo(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7], 
                    lugar=atividade[8]
                ))
            elif atividade[6] == TipoAtividadeEnum().REVISAO:
                result.append(Revisao(
                    id=atividade[0], 
                    nome=atividade[1], 
                    data=atividade[2], 
                    disciplina_id=atividade[5], 
                    observacao=atividade[7], 
                    materia=atividade[10]
                ))
            else:   
                raise ValueError("Tipo de atividade inválido")
        result.sort(key=lambda atv: datetime.strptime(atv.data, "%d/%m/%Y"))
        return result
    
    def listar_semana(self, semestre:"SemestreService"):
        """Lista todas as atividades de um semestre específico que ocorrem na semana atual."""
        atividades = self.listar_por_semestre(semestre)
        if not atividades:
            return []
        hoje = datetime.today()
        domingo = hoje - timedelta(days=hoje.weekday() + 1)  if hoje.weekday!=6 else hoje 
        domingo = domingo.replace(hour=0, minute=0, second=0, microsecond=0)
        sabado = domingo + timedelta(days=6)
        result = []
        for atividade in atividades:
            data_atividade = datetime.strptime(atividade.data, "%d/%m/%Y")
            if domingo <= data_atividade <= sabado:
                result.append(atividade)
        
        return result


