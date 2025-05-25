from typing import Optional
from app.models.disciplinas import Disciplina
class Semestre:
    def __init__(
    self, 
    nome: str, 
    data_inicio: str, 
    data_fim: str, 
    id: Optional[int]=None
    ):
        self._id = id
        self._nome = nome
        self._data_inicio = data_inicio
        self._data_fim = data_fim
        self._disciplinas = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        self._nome = nome

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def data_inicio(self):
        return self._data_inicio
    
    @data_inicio.setter
    def data_inicio(self, data_inicio: str):
        self._data_inicio = data_inicio

    @property
    def data_fim(self):
        return self._data_fim
    
    @data_fim.setter
    def data_fim(self, data_fim: str):
        self._data_fim = data_fim

    @property
    def disciplinas(self):
        return self._disciplinas
    
    @disciplinas.setter
    def disciplinas(self, disciplinas: list[Disciplina]):
        self._disciplinas = disciplinas
    
    def adicionar_disciplina(self, disciplina: "Disciplina"):
        self._disciplinas.append(disciplina)

   
    def listar_disciplinas(self):
        for disciplina in self._disciplinas:
            print(f"Disciplina: {disciplina.nome}, Carga Horária: {disciplina.carga_horaria}, Código: {disciplina.codigo}, Observação: {disciplina.observacao}, Id: {disciplina.id}")
