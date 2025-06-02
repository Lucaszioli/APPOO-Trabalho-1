from typing import Optional
from app.models.disciplinas import Disciplina
from datetime import datetime
class Semestre:
    def __init__(
    self, 
    nome: str, 
    data_inicio: str, 
    data_fim: str, 
    id: Optional[int]=None,
    nsg: Optional[float]=None,
    ):
        if not nome:
            raise ValueError("Nome do semestre não pode ser vazio.")
        if not isinstance(nome, str):
            raise ValueError("Nome do semestre deve ser uma string.")
        if not data_inicio:
            raise ValueError("Data de início não pode ser vazia.")
        if not isinstance(data_inicio, str):
            raise ValueError("Data de início deve ser uma string.")
        if not data_fim:
            raise ValueError("Data de fim não pode ser vazia.")
        inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
        fim = datetime.strptime(data_fim, "%d/%m/%Y")
        if fim <= inicio:
            raise ValueError("Data de fim deve ser posterior à data de início.")
        self._id = id
        self._nome = nome
        self._data_inicio = data_inicio
        self._data_fim = data_fim
        self._disciplinas = []
        self._nsg = nsg

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        if not nome:
            raise ValueError("Nome do semestre não pode ser vazio.")
        if not isinstance(nome, str):
            raise ValueError("Nome do semestre deve ser uma string.")
        self._nome = nome

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id: int):
        if id is not None and (not isinstance(id, int) or id <= 0):
            raise ValueError("ID do semestre deve ser um número inteiro positivo.")
        if self._id is not None:
            raise ValueError("ID já está definido e não pode ser alterado.")
        self._id = id

    @property
    def data_inicio(self):
        return self._data_inicio
    
    @data_inicio.setter
    def data_inicio(self, data_inicio: str):
        if not data_inicio:
            raise ValueError("Data de início não pode ser vazia.")
        if not isinstance(data_inicio, str):
            raise ValueError("Data de início deve ser uma string.")
        try:
            datetime.strptime(data_inicio, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Data de início deve estar no formato 'dd/mm/yyyy'.")
        if self._data_fim and datetime.strptime(data_inicio, "%d/%m/%Y") >= datetime.strptime(self._data_fim, "%d/%m/%Y"):
            raise ValueError("Data de início deve ser anterior à data de fim.")
        self._data_inicio = data_inicio

    @property
    def data_fim(self):
        return self._data_fim
    
    @data_fim.setter
    def data_fim(self, data_fim: str):
        if not data_fim:
            raise ValueError("Data de fim não pode ser vazia.")
        if not isinstance(data_fim, str):
            raise ValueError("Data de fim deve ser uma string.")
        try:
            datetime.strptime(data_fim, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Data de fim deve estar no formato 'dd/mm/yyyy'.")
        if self._data_inicio and datetime.strptime(data_fim, "%d/%m/%Y") <= datetime.strptime(self._data_inicio, "%d/%m/%Y"):
            raise ValueError("Data de fim deve ser posterior à data de início.")
        
        self._data_fim = data_fim

    @property
    def disciplinas(self):
        return self._disciplinas
    
    @disciplinas.setter
    def disciplinas(self, disciplinas: list[Disciplina]):
        self._disciplinas = disciplinas

    @property
    def nsg(self):
        return self._nsg
    
    @nsg.setter
    def nsg(self, nsg: int):
        if nsg is not None and (not isinstance(nsg, float) or nsg < 0):
            raise ValueError("NSG deve ser um número inteiro não negativo.")
        self._nsg = nsg
    
    def adicionar_disciplina(self, disciplina: "Disciplina") -> None:
        if not isinstance(disciplina, Disciplina):
            raise ValueError("Disciplina deve ser uma instância da classe Disciplina.")
        self._disciplinas.append(disciplina)
   
    def remover_disciplina(self, disciplina: "Disciplina"):
        if disciplina not in self._disciplinas:
            raise ValueError("Disciplina não encontrada no semestre.")
        if not isinstance(disciplina, Disciplina):
            raise ValueError("Disciplina deve ser uma instância da classe Disciplina.")
        self._disciplinas.remove(disciplina)