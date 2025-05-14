from app.views.base_window import BaseWindow
from app.components.disciplinas_frame import DisciplinasFrame

class PaginaSemestre(BaseWindow):
    """Janela de detalhes de um semestre específico."""

    def __init__(self, semestre, conexao, semestre_service):
        self.semestre = semestre
        super().__init__(conexao, title=f"Semestre {semestre.nome}", semestre_service=semestre_service)

    def _create_body(self) -> None:
        sem_frame = DisciplinasFrame(self.conexao, semestre=self.semestre, semestre_service=self.semestre_service, master=self)
        sem_frame.configure(corner_radius=0)
        sem_frame.grid(row=0, column=1, sticky="nsew")
