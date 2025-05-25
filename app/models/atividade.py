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
        tipo: Optional[TipoAtividadeEnum] = None
        ):
        self._id = id
        self._nome = nome
        self._data = data
        self._disciplina_id = disciplina_id
        self._observacao = observacao
        self._tipo = tipo

    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:
        self._id = id

    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, nome: str) -> None:
        self._nome = nome

    @property
    def data(self) -> str:
        return self._data
    
    @data.setter
    def data(self, data: str) -> None:
        self._data = data

    @property
    def disciplina_id(self) -> int:
        return self._disciplina_id
    
    @disciplina_id.setter
    def disciplina_id(self, disciplina_id: int) -> None:
        self._disciplina_id = disciplina_id

    @property
    def observacao(self) -> Optional[str]:
        return self._observacao
    
    @observacao.setter
    def observacao(self, observacao: str) -> None:
        self._observacao = observacao


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
        super().__init__(nome, data, disciplina_id, observacao, id)
        self._tipo = TipoAtividadeEnum().TRABALHO
        self._data_apresentacao = data_apresentacao
        self._nota_total = nota_total
        self._nota = nota

    @property
    def data_apresentacao(self) -> Optional[str]:
        return self._data_apresentacao
    
    @data_apresentacao.setter
    def data_apresentacao(self, data_apresentacao: str) -> None:
        self._data_apresentacao = data_apresentacao
    
    @property
    def nota_total(self) -> Optional[float]:
        return self._nota_total
    
    @nota_total.setter
    def nota_total(self, nota_total: float) -> None:
        self._nota_total = nota_total

    @property
    def nota(self) -> Optional[float]:
        return self._nota
    
    @nota.setter
    def nota(self, nota: float) -> None:
        self._nota = nota
    
        

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
        super().__init__(nome, data, disciplina_id, observacao, id)
        self._tipo = TipoAtividadeEnum().PROVA
        self._nota_total = nota_total
        self._nota = nota

    @property
    def nota_total(self) -> Optional[float]:
        return self._nota_total
    
    @nota_total.setter
    def nota_total(self, nota_total: float) -> None:
        self._nota_total = nota_total

    @property
    def nota(self) -> Optional[float]:
        return self._nota
    
    @nota.setter
    def nota(self, nota: float) -> None:
        self._nota = nota


    

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
        self.lugar = lugar

    @property
    def lugar(self) -> str:
        return self._lugar
    
    @lugar.setter
    def lugar(self, lugar: str) -> None:
        self._lugar = lugar


class Revisao(Atividade):
    def __init__(
        self, 
        nome: str, 
        data: str, 
        disciplina_id: str,
        materia: Optional[str] = None,
        observacao: Optional[str] = None, 
        id: Optional[str]=None
        ):
        super().__init__(nome, data, disciplina_id, observacao, id)
        self._tipo = TipoAtividadeEnum().REVISAO
        self._materia = materia

    @property
    def materia(self) -> Optional[str]:
        return self._materia
    
    @materia.setter
    def materia(self, materia: str) -> None:
        self._materia = materia