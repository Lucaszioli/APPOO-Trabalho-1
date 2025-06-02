from abc import ABC
from typing import Optional
from datetime import datetime
from app.errors.incorrectDate import incorrectDate
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
        tipo: Optional[TipoAtividadeEnum] = None,
        progresso: Optional[str] = 'Não começou'
        ):
        if not nome:
            raise ValueError("Nome da atividade não pode ser vazio.")
        if not isinstance(nome, str):
            raise ValueError("Nome da atividade deve ser uma string.")
        if not data:
            raise ValueError("Data da atividade não pode ser vazia.")
        if not isinstance(data, str):
            raise ValueError("Data da atividade deve ser uma string.")
        if not isinstance(disciplina_id, int) or disciplina_id <= 0:
            raise ValueError("ID da disciplina deve ser um número inteiro positivo.")
        if id is not None and (not isinstance(id, int) or id <= 0):
            raise ValueError("ID da atividade deve ser um número inteiro positivo.")
        
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Data da atividade deve estar no formato 'dd/mm/yyyy'.")
        
        self._id = id
        self._nome = nome
        self._data = data
        self._disciplina_id = disciplina_id
        self._observacao = observacao
        self._tipo = tipo
        self._progresso = progresso

    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:
        if id is not None and (not isinstance(id, int) or id <= 0):
            raise ValueError("ID da atividade deve ser um número inteiro positivo.")
        if self._id is not None:
            raise ValueError("ID já está definido e não pode ser alterado.")
        self._id = id

    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, nome: str) -> None:
        if not nome:
            raise ValueError("Nome da atividade não pode ser vazio.")
        if not isinstance(nome, str):
            raise ValueError("Nome da atividade deve ser uma string.")
        self._nome = nome

    @property
    def data(self) -> str:
        return self._data
    
    @data.setter
    def data(self, data: str) -> None:
        if not data:
            raise ValueError("Data da atividade não pode ser vazia.")
        if not isinstance(data, str):
            raise ValueError("Data da atividade deve ser uma string.")
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Data da atividade deve estar no formato 'dd/mm/yyyy'.")

        self._data = data

    @property
    def disciplina_id(self) -> int:
        return self._disciplina_id
    
    @disciplina_id.setter
    def disciplina_id(self, disciplina_id: int) -> None:
        if not isinstance(disciplina_id, int) or disciplina_id <= 0:
            raise ValueError("ID da disciplina deve ser um número inteiro positivo.")
        if self._disciplina_id is not None:
            raise ValueError("ID da disciplina já está definido e não pode ser alterado.")
        self._disciplina_id = disciplina_id

    @property
    def observacao(self) -> Optional[str]:
        return self._observacao
    
    @observacao.setter
    def observacao(self, observacao: str) -> None:
        self._observacao = observacao

    @property
    def tipo(self) -> Optional[TipoAtividadeEnum]:
        return self._tipo
    
    @tipo.setter
    def tipo(self, tipo) -> None:
        # Allow updates when the new value is the same as current value
        # This allows legitimate updates and prevents unintended type changes
        if self._tipo is not None and str(self._tipo) != str(tipo):
            # Only allow changes if both are string representations of the same type
            if hasattr(self, '_allow_tipo_update') and self._allow_tipo_update:
                pass  # Allow the update during editing
            else:
                raise ValueError("Tipo de atividade já está definido e não pode ser alterado.")
        self._tipo = tipo

    @property
    def progresso(self) -> str:
        return self._progresso
    
    @progresso.setter
    def progresso(self, progresso: str) -> None:
        if progresso not in ['Não começou', 'Em andamento', 'Concluída', 'Entregue']:
            raise ValueError("Progresso inválido.")
        self._progresso = progresso

class Trabalho(Atividade):
    def __init__(
        self, 
        nome: str, 
        data: str, 
        disciplina_id: int, 
        nota_total: Optional[float], 
        data_apresentacao: Optional[str] = None, 
        nota: Optional[float] = None, 
        observacao: Optional[str] = None, 
        id: Optional[int] = None,
        progresso: Optional[str] = 'Não começou'
        ):
        if nota_total <= 0:
            raise ValueError("Nota total deve ser um número positivo.")
        if nota is not None and (nota < 0 or nota > nota_total):
            raise ValueError("Nota deve ser um número entre 0 e a nota total.")
        if nota is not None and not isinstance(nota, float):
            raise ValueError("Nota deve ser um número.")
        if nota_total is not None and not isinstance(nota_total, float):
            raise ValueError("Nota total deve ser um número.")
        if data_apresentacao is not None and not isinstance(data_apresentacao, str):
            raise ValueError("Data de apresentação deve ser uma string.")
        super().__init__(nome, data, disciplina_id, observacao, id, tipo=TipoAtividadeEnum().TRABALHO, progresso=progresso)
        if data_apresentacao:
            try:
                datetime.strptime(data_apresentacao, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Data de apresentação deve estar no formato 'dd/mm/yyyy'.")
            apresentacao = datetime.strptime(data_apresentacao, "%d/%m/%Y")
            if apresentacao < datetime.strptime(data, "%d/%m/%Y"):
                raise incorrectDate("Data de apresentação não pode ser anterior à data da atividade.")
        self._tipo = TipoAtividadeEnum().TRABALHO
        self._data_apresentacao = data_apresentacao
        self._nota_total = nota_total
        self._nota = nota

    @property
    def data_apresentacao(self) -> Optional[str]:
        return self._data_apresentacao
    
    @data_apresentacao.setter
    def data_apresentacao(self, data_apresentacao: str) -> None:
        if data_apresentacao is not None and not isinstance(data_apresentacao, str):
            raise ValueError("Data de apresentação deve ser uma string.")
        if data_apresentacao is not None and not data_apresentacao:
            raise ValueError("Data de apresentação não pode ser vazia.")
        try:
            datetime.strptime(data_apresentacao, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Data de apresentação deve estar no formato 'dd/mm/yyyy'.")
        if self._data and datetime.strptime(data_apresentacao, "%d/%m/%Y") < datetime.strptime(self._data, "%d/%m/%Y"):
            raise incorrectDate("Data de apresentação não pode ser anterior à data da atividade.")
        self._data_apresentacao = data_apresentacao
    
    @property
    def nota_total(self) -> Optional[float]:
        return self._nota_total
    
    @nota_total.setter
    def nota_total(self, nota_total: float) -> None:
        if nota_total is not None and nota_total <= 0:
            raise ValueError("Nota total deve ser um número positivo.")
        if self._nota is not None and (self._nota < 0 or self._nota > nota_total):
            raise ValueError("Nota deve ser um número entre 0 e a nota total.")
        if nota_total is not None and not isinstance(nota_total, float):
            raise ValueError("Nota total deve ser um número.")
        self._nota_total = nota_total

    @property
    def nota(self) -> Optional[float]:
        return self._nota
    
    @nota.setter
    def nota(self, nota: float) -> None:
        if nota is not None and (nota < 0 or nota > self._nota_total):
            raise ValueError("Nota deve ser um número entre 0 e a nota total.")
        if nota is not None and not isinstance(nota, float):
            raise ValueError("Nota deve ser um número.")
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
        id: Optional[int]=None,
        progresso: Optional[str] = 'Não começou'
        ):
        super().__init__(nome, data, disciplina_id, observacao, id, tipo=TipoAtividadeEnum().PROVA, progresso=progresso)
        if nota_total <= 0:
            raise ValueError("Nota total deve ser um número positivo.")
        if nota is not None and (nota < 0 or nota > nota_total):
            raise ValueError("Nota deve ser um número entre 0 e a nota total.")
        if nota is not None and not isinstance(nota, float):
            raise ValueError("Nota deve ser um número.")
        if nota_total is not None and not isinstance(nota_total, float):
            raise ValueError("Nota total deve ser um número.")
        if not nota_total:
            raise ValueError("Nota total não pode ser vazia.")
        self._tipo = TipoAtividadeEnum().PROVA
        self._nota_total = nota_total
        self._nota = nota

    @property
    def nota_total(self) -> float:
        return self._nota_total
    
    @nota_total.setter
    def nota_total(self, nota_total: float) -> None:
        if nota_total <= 0:
            raise ValueError("Nota total deve ser um número positivo.")
        if self._nota is not None and (self._nota < 0 or self._nota > nota_total):
            raise ValueError("Nota deve ser um número entre 0 e a nota total.")
        if nota_total is not None and not isinstance(nota_total, float):
            raise ValueError("Nota total deve ser um número.")
        if not nota_total:
            raise ValueError("Nota total não pode ser vazia.")
        self._nota_total = nota_total

    @property
    def nota(self) -> Optional[float]:
        return self._nota
    
    @nota.setter
    def nota(self, nota: float) -> None:
        if nota is not None and (nota < 0 or nota > self._nota_total):
            raise ValueError("Nota deve ser um número entre 0 e a nota total.")
        if nota is not None and not isinstance(nota, float):
            raise ValueError("Nota deve ser um número.")
        if self._nota is not None and (self._nota < 0 or self._nota > self._nota_total):
            raise ValueError("Nota deve ser um número entre 0 e a nota total.")
        self._nota = nota


    

class Aula_de_Campo(Atividade):
    def __init__(
        self, 
        nome: str, 
        data: str, 
        disciplina_id: int, 
        lugar: Optional[str], 
        observacao: Optional[str] = None, 
        id: Optional[int]=None,
        progresso: Optional[str] = 'Não começou'
        ):
        super().__init__(nome, data, disciplina_id, observacao, id, tipo=TipoAtividadeEnum().CAMPO, progresso=progresso)
        if lugar and not isinstance(lugar, str):
            raise ValueError("Lugar deve ser uma string.")
        self._tipo = TipoAtividadeEnum().CAMPO
        self._lugar = lugar

    @property
    def lugar(self) -> Optional[str]:
        return self._lugar
    
    @lugar.setter
    def lugar(self, lugar: str) -> None:
        if lugar is not None and not isinstance(lugar, str):
            raise ValueError("Lugar deve ser uma string.")
        self._lugar = lugar


class Revisao(Atividade):
    def __init__(
        self, 
        nome: str, 
        data: str, 
        disciplina_id: str,
        materia: Optional[str] = None,
        observacao: Optional[str] = None, 
        id: Optional[str]=None,
        progresso: Optional[str] = 'Não começou'
        ):
        super().__init__(nome, data, disciplina_id, observacao, id, tipo=TipoAtividadeEnum().REVISAO, progresso=progresso)
        self._tipo = TipoAtividadeEnum().REVISAO
        if materia is not None and not isinstance(materia, str):
            raise ValueError("Matéria deve ser uma string.")
            
        self._materia = materia

    @property
    def materia(self) -> Optional[str]:
        return self._materia
    
    @materia.setter
    def materia(self, materia: str) -> None:
        if materia is not None and not isinstance(materia, str):
            raise ValueError("Matéria deve ser uma string.")
        self._materia = materia