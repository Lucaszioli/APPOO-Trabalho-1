from typing import Optional
from app.models.atividade import Atividade
class Disciplina:
    def __init__(
        self, 
        nome: str, 
        carga_horaria: int, 
        semestre_id:int, 
        codigo:str, 
        observacao: Optional[str] = None, 
        id:Optional[int] = None
        ):
        if not nome:
            raise ValueError("Nome da disciplina não pode ser vazio.")
        if not isinstance(nome, str):
            raise ValueError("Nome da disciplina deve ser uma string.")
        if not isinstance(carga_horaria, int) or carga_horaria <= 0:
            raise ValueError("Carga horária deve ser um número inteiro positivo.")
        if not isinstance(semestre_id, int) or semestre_id <= 0:
            raise ValueError("ID do semestre deve ser um número inteiro positivo.")
        if not codigo:
            raise ValueError("Código da disciplina não pode ser vazio.")
        if not isinstance(codigo, str):
            raise ValueError("Código da disciplina deve ser uma string.")
        self._nome = nome
        self._carga_horaria = carga_horaria
        self._semestre_id = semestre_id
        self._atividades : list[Atividade] = []
        self._codigo = codigo
        self._observacao = observacao
        self._id = id

    @property
    def nome(self) -> str:
        return self._nome
    @nome.setter
    def nome(self, nome: str) -> None:
        if not nome:
            raise ValueError("Nome da disciplina não pode ser vazio.")
        if not isinstance(nome, str):
            raise ValueError("Nome da disciplina deve ser uma string.")
        self._nome = nome

    @property
    def carga_horaria(self) -> int:
        return self._carga_horaria
    
    @carga_horaria.setter
    def carga_horaria(self, carga_horaria: int) -> None:
        if not isinstance(carga_horaria, int) or carga_horaria <= 0:
            raise ValueError("Carga horária deve ser um número inteiro positivo.")
        self._carga_horaria = carga_horaria
    
    @property
    def semestre_id(self) -> int:
        return self._semestre_id
    
    @semestre_id.setter
    def semestre_id(self, semestre_id: int) -> None:
        if not isinstance(semestre_id, int) or semestre_id <= 0:
            raise ValueError("ID do semestre deve ser um número inteiro positivo.")
        if self._semestre_id is not None:
            raise ValueError("ID do semestre já está definido e não pode ser alterado.")
        self._semestre_id = semestre_id

    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:
        if id is not None and (not isinstance(id, int) or id <= 0):
            raise ValueError("ID deve ser um número inteiro positivo.")
        if self._id is not None:
            raise ValueError("ID já está definido e não pode ser alterado.")
        self._id = id

    @property
    def codigo(self) -> str:
        return self._codigo
    
    @codigo.setter
    def codigo(self, codigo: str) -> None:
        if not codigo:
            raise ValueError("Código da disciplina não pode ser vazio.")
        if not isinstance(codigo, str):
            raise ValueError("Código da disciplina deve ser uma string.")
        self._codigo = codigo

    @property
    def observacao(self) -> Optional[str]:
        return self._observacao
    
    @observacao.setter
    def observacao(self, observacao: str) -> None:
        self._observacao = observacao
    
    @property
    def atividades(self) -> list[Atividade]:
        return self._atividades
    
    @atividades.setter
    def atividades(self, atividades: list[Atividade]) -> None:
        if not isinstance(atividades, list):
            raise ValueError("Atividades deve ser uma lista.")
        self._atividades = atividades
    
    def adicionar_atividade(self, atividade: "Atividade") -> None:
        if not isinstance(atividade, Atividade):
            raise ValueError("Atividade deve ser uma instância da classe Atividade.")
        self._atividades.append(atividade)

    def remover_atividade(self, atividade: "Atividade") -> None:
        if atividade not in self._atividades:
            raise ValueError("Atividade não encontrada na disciplina.")
        if not isinstance(atividade, Atividade):
            raise ValueError("Atividade deve ser uma instância da classe Atividade.")
        self._atividades.remove(atividade)

    def listar_atividades(self) -> None:
        for atividade in self.atividades:
            print(f"Atividade: {atividade.nome}, Data: {atividade.data}, Nota Total: {atividade.nota_total}, Observação: {atividade.observacao}")
    
    
    