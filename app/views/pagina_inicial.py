from app.views.base_window import BaseWindow
from app.components.semestres_frame import SemestresFrame

class PaginaInicial(BaseWindow):
    """Janela principal que lista todos os semestres disponíveis."""

    def __init__(self, conexao, semestre_service):
        super().__init__(conexao, title="Sistema de Gerenciamento Acadêmico", semestre_service=semestre_service)

    def _create_body(self) -> None:
        sem_frame = SemestresFrame(self.conexao, self.semestre_service, semestre=None, master=self)
        sem_frame.configure(corner_radius=0)
        sem_frame.grid(row=0, column=1, sticky="nsew")
