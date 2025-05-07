from app.views.base_window import BaseWindow
from app.components.disciplinas_frame import DisciplinasFrame

class PaginaSemestre(BaseWindow):
    """Janela de detalhes de um semestre específico."""

    def __init__(self, semestre, conexao):
        self.semestre = semestre
        super().__init__(conexao, title=f"Semestre {semestre.nome}")

    def _create_body(self) -> None:
        sem_frame = DisciplinasFrame(self.conexao, semestre=self.semestre, master=self)
        sem_frame.grid(row=0, column=1, sticky="nsew")
