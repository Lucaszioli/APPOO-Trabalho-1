from abc import ABC, abstractmethod
from app.utils.database import Database
from app.models.disciplinas import Disciplina
from app.models.atividade import Atividade, Trabalho, Prova, Aula_de_Campo, Revisao,TipoAtividadeEnum
from typing import Optional
from app.errors.notFound import AtividadeNotFoundError
class AtividadeService(ABC, Database):

    def __init__(self, db_path="db.db"):
        super().__init__(db_path)

    def _adicionar_bd(self, atividade:"Atividade") -> Atividade:
        self.query = "INSERT INTO atividade (nome, data, disciplina_id, tipo, nota_total, nota, observacao, lugar, data_apresentacao, materia) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
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
            getattr(atividade, "materia", None)
            )
        atividade.id = self._adicionar(self.query, self.params)
        return atividade
    
    def listar(self) -> list[Atividade]:
        self.query = "SELECT * FROM atividade"
        self.params = ()
        atividades = self._buscar_varios(self.query, self.params)
        if not atividades:
            return []
        return [Atividade(id=row[0], nome=row[1], data=row[2], nota=row[3], nota_total=row[4], disciplina_id=row[5], tipo=row[6], observacao=row[7], lugar=row[8], data_apresentacao=row[9]) for row in atividades]
    
    def listar_por_disciplina(self, disciplina:"Disciplina") -> list[Atividade]:
        self.query = "SELECT * FROM atividade WHERE disciplina_id = ?"
        self.params = (disciplina.id,)
        atividades = self._buscar_varios(self.query, self.params)
        if not atividades:
            return []
        
        return [Atividade(id=row[0], nome=row[1], data=row[2], nota=row[3], nota_total=row[4], disciplina_id=row[5], tipo=row[6], observacao=row[7], lugar=row[8], data_apresentacao=row[9]) for row in atividades] 

    
    def buscar_por_id(self, id:str) -> Optional[Atividade]:
        self.query = "SELECT * FROM atividade WHERE id = ?"
        self.params = (id,)
        atividade = self._buscar_um(self.query, self.params)
        if atividade:
            if atividade[6] == TipoAtividadeEnum().TRABALHO:
                return Trabalho(id=atividade[0], nome=atividade[1], data=atividade[2], disciplina_id=atividade[5], nota_total=atividade[4], nota=atividade[3], observacao=atividade[7], data_apresentacao=atividade[9])
            elif atividade[6] == TipoAtividadeEnum().PROVA:
                return Prova(id=atividade[0], nome=atividade[1], data=atividade[2], disciplina_id=atividade[5], nota_total=atividade[4], nota=atividade[3], observacao=atividade[7])
            elif atividade[6] == TipoAtividadeEnum().CAMPO:
                print(atividade)
                return Aula_de_Campo(id=atividade[0], nome=atividade[1], data=atividade[2], disciplina_id=atividade[5],observacao=atividade[7], lugar=atividade[8])
            elif atividade[6] == TipoAtividadeEnum().REVISAO:
                return Revisao(id=atividade[0], nome=atividade[1], data=atividade[2], disciplina_id=atividade[5], observacao=atividade[7], materia=atividade[10])
            else:   
                raise ValueError("Tipo de atividade inválido")
        return None
    
    def editar_bd(self, atividade:"Atividade") -> "Atividade":
        self.atividadeExistente = self.buscar_por_id(atividade.id)
        if not self.atividadeExistente:
            raise AtividadeNotFoundError()
        self.query = "UPDATE atividade SET nome = ?, data = ?, disciplina_id = ?, tipo = ?, nota_total = ?, nota = ?, observacao = ?, lugar = ?, data_apresentacao = ? WHERE id = ?"
        self.params = (atividade.nome, atividade.data, atividade.disciplina_id, atividade.tipo, atividade.nota_total, atividade.nota, atividade.observacao, atividade.lugar, atividade.data_apresentacao, atividade.id)
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
    
    def criar_atividade(self, nome:str, data:str, disciplina:"Disciplina",tipo:"TipoAtividadeEnum", nota_total:int, nota:int = None, observacao:str = None, lugar:str = None, data_apresentacao:str = None, materia=None) -> Atividade:
        if tipo == TipoAtividadeEnum().TRABALHO:
            atividade = Trabalho(nome, data, disciplina.id, nota_total, nota=nota, observacao=observacao, data_apresentacao=data_apresentacao)
        elif tipo == TipoAtividadeEnum().PROVA:
            atividade = Prova(nome, data, disciplina.id, nota_total, nota=nota, observacao=observacao)
        elif tipo == TipoAtividadeEnum().CAMPO:
            atividade = Aula_de_Campo(nome, data, disciplina.id, lugar=lugar, observacao=observacao)
        elif tipo == TipoAtividadeEnum().REVISAO:
            atividade = Revisao(nome, data, disciplina.id, observacao=observacao, materia=materia)
        else:
            raise ValueError("Tipo de atividade inválido")
        
        self._adicionar_bd(atividade)
        disciplina.adicionar_atividade(atividade)
        return atividade


