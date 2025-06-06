from app.ui.views.base_window import BaseWindow
from typing import Any

class PaginaDisciplina(BaseWindow):
    """"Janela de detalhes de uma disciplina específica."""
    def __init__(self, disciplina: Any, service: Any) -> None:
        self.disciplina = disciplina
        title = f"Disciplina: {disciplina.nome}"
        super().__init__(
            title=title,
            service=service
        )

    def _create_body(self) -> None:
        try:
            from app.ui.listframes.listframe_atividades import AtividadesFrame
            
            self.atividades_frame = AtividadesFrame(
                disciplina=self.disciplina,
                service=self.service,
                master=self
            )
            self.atividades_frame.configure(corner_radius=0)
            self.atividades_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        except Exception as e:
            self.show_error_message(
                "Erro de Inicialização",
                f"Não foi possível carregar os detalhes da disciplina: {str(e)}"
            )

    def show_frame(self, atividade):
        if hasattr(self, 'disciplinas_frame') and self.disciplinas_frame:
            self.disciplinas_frame.destroy()
        elif hasattr(self, 'atividades_frame') and self.atividades_frame:
            self.atividades_frame.destroy()
            
        from app.ui.listframes.listframe_atividades import AtividadesFrame
        
        self.atividades_frame = AtividadesFrame(
            disciplina=self.disciplina,
            service=self.service,
            master=self
        )
        self.atividades_frame.configure(corner_radius=0)
        self.atividades_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)