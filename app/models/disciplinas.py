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
        id = None
        ):
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.semestre_id = semestre_id
        self.atividades = []
        self.codigo = codigo
        self.observacao = observacao
        self.id = id

    def adicionar_atividade(
    self, 
    atividade: "Atividade"
    ):
        self.atividades.append(atividade)

    def listar_atividades(self):
        for atividade in self.atividades:
            print(f"Atividade: {atividade.nome}, Data: {atividade.data}, Nota Total: {atividade.nota_total}, Observação: {atividade.observacao}")
    
    
    