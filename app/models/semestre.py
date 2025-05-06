from app.models.disciplinas import Disciplina
from app.services.semestre_services import SemestreService
class Semestre:
    def __init__(self, nome, data_inicio, data_fim, id=None):
        self.id = id
        self.nome = nome
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.disciplinas = []

    def set_nome(self, nome):
        self.nome = nome
    
    def set_data_inicio(self, data_inicio):
        self.data_inicio = data_inicio
    
    def set_data_fim(self, data_fim):
        self.data_fim = data_fim
    
    def adicionar_disciplina(self, disciplina):
        self.disciplinas.append(disciplina)
   
    def listar_disciplinas(self):
        for disciplina in self.disciplinas:
            print(f"Disciplina: {disciplina.nome}, Carga Horária: {disciplina.carga_horaria}, Código: {disciplina.codigo}, Observação: {disciplina.observacao}, Id: {disciplina.id}")

    def adicionar_bd(self, conexao):
        SemestreService.adicionar_bd(self, conexao)


    def editar_bd(self, conexao):
        SemestreService.editar_bd(self, conexao)
    
    def deletar_bd(self, conexao):
        SemestreService.deletar_bd(self, conexao)
    
    
    @staticmethod
    def listar_semestres(conexao):
        return SemestreService.listar_semestres(conexao)
    
    @staticmethod
    def buscar_ultimo_semestre(conexao):
        return SemestreService.buscar_ultimo_semestre
    
    def carregar_disciplinas(self, conexao):
        SemestreService.carregar_disciplinas(self, conexao)
