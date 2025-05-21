from app.services.semestre_services import SemestreService
from app.services.disciplinas_services import DisciplinaService
class ServiceUniversal :
    def __init__(self, semestre_service:"SemestreService", disciplina_service:"DisciplinaService"):
        self.semestre_service = semestre_service
        self.disciplina_service = disciplina_service
        # self.atividade_service = atividade_service