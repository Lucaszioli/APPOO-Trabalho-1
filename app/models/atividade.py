from abc import ABC
from typing import Optional

class TipoAtividadeEnum:
    def __init__(self):
        self.TRABALHO = "Trabalho"
        self.PROVA = "Prova"
        self.CAMPO = "Aula de campo"
        self.REVISAO = "Aula de revisão"


class Atividade(ABC):
    def __init__(
        self, 
        nome: str,
        data: str,
        disciplina_id: int, 
        observacao: Optional[str] = None, 
        id: Optional[int]=None, 
        lugar: Optional[str] = None, 
        data_apresentacao: Optional[str] = None, 
        nota_total: Optional[float] = None, 
        nota: Optional[float] = None, 
        tipo: Optional[TipoAtividadeEnum] = None
        ):
        self.id = id
        self.nome = nome
        self.data = data
        self.disciplina_id = disciplina_id
        self.observacao = observacao
        self.lugar = lugar
        self.data_apresentacao = data_apresentacao
        self.nota_total = nota_total
        self.nota = nota
        self.tipo = tipo


class Trabalho(Atividade):
    def __init__(
        self, 
        nome: str, 
        data: str, 
        disciplina_id: int, 
        nota_total: float, 
        data_apresentacao: Optional[str] = None, 
        nota: Optional[float] = None, 
        observacao: Optional[str] = None, 
        id: Optional[int] = None
        ):
        super().__init__(nome, data, disciplina_id, observacao, id, data_apresentacao=data_apresentacao, nota_total=nota_total, nota=nota)
        self.tipo = TipoAtividadeEnum().TRABALHO
        

class Prova(Atividade):
    def __init__(
        self, 
        nome: str, 
        data: str, 
        disciplina_id: int, 
        nota_total: float, 
        nota: Optional[float] = None, 
        observacao: Optional[float] = None, 
        id: Optional[int]=None
        ):
        super().__init__(nome, data, disciplina_id, observacao, id, nota_total=nota_total, nota=nota)
        self.tipo = TipoAtividadeEnum().PROVA

class Aula_de_Campo(Atividade):
    def __init__(
        self, 
        nome: str, 
        data: str, 
        disciplina_id: int, 
        lugar: str, 
        observacao: Optional[str] = None, 
        id: Optional[int]=None
        ):
        super().__init__(nome, data, disciplina_id, observacao, id, lugar=lugar)
        self.tipo = TipoAtividadeEnum().CAMPO


class Revisao(Atividade):
    def __init__(
        self, 
        nome: str, 
        data: str, 
        disciplina_id: str, 
        observacao: Optional[str] = None, 
        id: Optional[str]=None
        ):
        super().__init__(nome, data, disciplina_id, observacao, id)
        self.tipo = TipoAtividadeEnum().REVISAO
        