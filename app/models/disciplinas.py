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
        self._nome = nome
        self._carga_horaria = carga_horaria
        self._semestre_id = semestre_id
        self._atividades = []
        self._codigo = codigo
        self._observacao = observacao
        self._id = id

    @property
    def nome(self) -> str:
        return self._nome
    @nome.setter
    def nome(self, nome: str) -> None:
        self._nome = nome

    @property
    def carga_horaria(self) -> int:
        return self._carga_horaria
    
    @carga_horaria.setter
    def carga_horaria(self, carga_horaria: int) -> None:
        self._carga_horaria = carga_horaria
    
    @property
    def semestre_id(self) -> int:
        return self._semestre_id
    
    @semestre_id.setter
    def semestre_id(self, semestre_id: int) -> None:
        self._semestre_id = semestre_id

    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:
        self._id = id

    @property
    def codigo(self) -> str:
        return self._codigo
    
    @codigo.setter
    def codigo(self, codigo: str) -> None:
        self._codigo = codigo

    @property
    def observacao(self) -> Optional[str]:
        return self._observacao
    
    @observacao.setter
    def observacao(self, observacao: str) -> None:
        self._observacao = observacao
    

    def adicionar_atividade(
    self, 
    atividade: "Atividade"
    ) -> None:
        self._atividades.append(atividade)

    def listar_atividades(self) -> None:
        for atividade in self.atividades:
            print(f"Atividade: {atividade.nome}, Data: {atividade.data}, Nota Total: {atividade.nota_total}, Observação: {atividade.observacao}")
    
    
    