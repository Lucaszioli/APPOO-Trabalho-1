from abc import ABC, abstractmethod
from app.utils.database import Database
from app.models.disciplinas import Disciplina
from app.models.atividade import Atividade, Trabalho, Prova, Aula_de_Campo, Revisao,TipoAtividadeEnum
from typing import Type
from app.errors.notFound import AtividadeNotFoundError
class AtividadeService(ABC, Database):

    def __init__(self, db_path="db.db"):
        super().__init__(db_path)

    def _adicionar_bd(self, atividade:Type[Atividade]) -> Type[Atividade]:
        self.query = "INSERT INTO atividade (nome, data, disciplina_id, tipo, nota_total, nota, observacao, lugar, data_apresentacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.params = (atividade.nome, atividade.data,atividade.disciplina_id, atividade.tipo, atividade.nota_total, atividade.nota, atividade.observacao, atividade.lugar, atividade.data_apresentacao)
        self._adicionar(self.query, self.params)
        return atividade
    
    def listar(self) -> list[Atividade]:
        self.query = "SELECT * FROM atividade"
        self.params = ()
        atividades = self._buscar_varios    (self.query, self.params)
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

    
    def buscar_por_id(self, id:str) -> Type[Atividade]:
        self.query = "SELECT * FROM atividade WHERE id = ?"
        self.params = (id,)
        atividade = self._buscar_um(self.query, self.params)
        if atividade:
            return Atividade(id=atividade[0], nome=atividade[1], data=atividade[2], nota=atividade[3], nota_total=atividade[4], disciplina_id=atividade[5], tipo=atividade[6], observacao=atividade[7], lugar=atividade[8], data_apresentacao=atividade[9])
        return None
    
    def editar_bd(self, atividade:Type[Atividade]) -> Type[Atividade]:
        self.atividadeExistente = self.buscar_por_id(atividade.id)
        if not self.atividadeExistente:
            raise AtividadeNotFoundError()
        self.query = "UPDATE atividade SET nome = ?, data = ?, disciplina_id = ?, tipo = ?, nota_total = ?, nota = ?, observacao = ?, lugar = ?, data_apresentacao = ? WHERE id = ?"
        self.params = (atividade.nome, atividade.data, atividade.disciplina_id, atividade.tipo, atividade.nota_total, atividade.nota, atividade.observacao, atividade.lugar, atividade.data_apresentacao, atividade.id)
        self._editar(self.query, self.params)
        return atividade
    
    def deletar(self, atividade:Type[Atividade]) -> Type[Atividade]:
        self.atividadeExistente = self.buscar_por_id(atividade.id)
        if not self.atividadeExistente:
            raise AtividadeNotFoundError()
        self.query = "DELETE FROM atividade WHERE id = ?"
        self.params = (atividade.id,)
        self.rows = self._deletar(self.query, self.params)
        del atividade
        return self.rows
    
    def criar_atividade(self, tipo:Type[Atividade], nome:str, data:str, disciplina:"Disciplina", nota_total:int, nota:int = None, observacao:str = None, lugar:str = None, data_apresentacao:str = None) -> Type[Atividade]:
        if tipo == TipoAtividadeEnum().TRABALHO:
            atividade = Trabalho(nome, data, disciplina.id, nota_total, nota=nota, observacao=observacao, data_apresentacao=data_apresentacao)
        elif tipo == TipoAtividadeEnum().PROVA:
            atividade = Prova(nome, data, disciplina.id, nota_total, nota=nota, observacao=observacao)
        elif tipo == TipoAtividadeEnum().CAMPO:
            atividade = Aula_de_Campo(nome, data, disciplina.id, lugar=lugar)
        elif tipo == TipoAtividadeEnum().REVISAO:
            atividade = Revisao(nome, data, disciplina.id, observacao=observacao)
        else:
            raise ValueError("Tipo de atividade inválido")
        return atividade


