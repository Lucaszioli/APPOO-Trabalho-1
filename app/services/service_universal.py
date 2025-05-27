from app.services.semestre_services import SemestreService
from app.services.disciplinas_services import DisciplinaService
from app.services.atividade_services import AtividadeService
class ServiceUniversal :
    def __init__(self, db_path="db.db"):
        self.semestre_service = SemestreService(db_path=db_path)
        self.disciplina_service = DisciplinaService(db_path=db_path)
        self.atividade_service = AtividadeService(db_path=db_path)
        # self.atividade_service = atividade_service