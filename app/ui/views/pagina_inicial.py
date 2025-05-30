from app.ui.views.base_window import BaseWindow
from app.ui.listframes.listframe_semestres import SemestresFrame
from app.ui.views.pagina_semestre import PaginaSemestre
from typing import Any
from app.ui.listframes.listframe_atividades import AtividadesFrame
from app.services.semestre_services import SemestreService

class PaginaInicial(BaseWindow):
    """Janela principal que lista todos os semestres disponíveis."""
    def __init__(self, conexao: Any, service: Any) -> None:
        super().__init__(
            conexao=conexao,
            title="Sistema de Gerenciamento Acadêmico",
            service=service
        )
        
    def _create_body(self) -> None:
        try:
            self.current_frame = SemestresFrame(
                conexao=self.conexao,
                service=self.service,
                semestre=None,
                master=self
            )
            self.current_frame.configure(corner_radius=0)
            self.current_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        except Exception as e:
            self.show_error_message(
                "Erro de Inicialização",
                f"Não foi possível carregar a lista de semestres: {str(e)}"
            )

    def show_frame(self, item):
        # Remove o frame atual, se existir
        if hasattr(self, 'current_frame') and self.current_frame:
            self.current_frame.destroy()
        from app.models.semestre import Semestre
        from app.models.disciplinas import Disciplina
        frame_kwargs = dict(conexao=self.conexao, service=self.service, master=self)
        show_back = True
        if hasattr(item, 'data_inicio') and hasattr(item, 'data_fim'):
            from app.ui.listframes.listframe_disciplinas import DisciplinasFrame
            self.current_frame = DisciplinasFrame(semestre=item, **frame_kwargs)
        elif hasattr(item, 'carga_horaria') and hasattr(item, 'nome'):
            self.current_frame = AtividadesFrame(disciplina=item, **frame_kwargs)
        else:
            from app.ui.listframes.listframe_semestres import SemestresFrame
            self.current_frame = SemestresFrame(semestre=None, **frame_kwargs)
            show_back = False
        self.current_frame.configure(corner_radius=0)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        # Botão de voltar na sidebar
        if hasattr(self, 'sidebar') and hasattr(self.sidebar, 'set_back_button'):
            self.sidebar.set_back_button(show_back, self._go_back)

    def _go_back(self):
        if hasattr(self.current_frame, 'semestre') and getattr(self.current_frame, 'semestre', None):
            self.show_frame(None)
        elif hasattr(self.current_frame, 'disciplina') and getattr(self.current_frame, 'disciplina', None):
            semestre = self.service.semestre_service.buscar_por_id(self.current_frame.disciplina.semestre_id)
            self.show_frame(semestre)
        else:
            return True
