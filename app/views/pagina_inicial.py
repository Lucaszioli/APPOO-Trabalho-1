from app.views.base_window import BaseWindow
from app.ui.listframe_semestres import SemestresFrame

class PaginaInicial(BaseWindow):
    """Janela principal melhorada que lista todos os semestres disponíveis."""

    def __init__(self, conexao, service):
        super().__init__(
            conexao=conexao,
            title="Sistema de Gerenciamento Acadêmico - Página Inicial",
            service=service
        )

    def _create_body(self) -> None:
        """Cria o corpo principal com frame de semestres."""
        try:
            # Frame principal de semestres
            self.sem_frame = SemestresFrame(
                conexao=self.conexao, 
                service=self.service, 
                semestre=None, 
                master=self
            )
            self.sem_frame.configure(corner_radius=0)
            self.sem_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
            
        except Exception as e:
            self.show_error_message(
                "Erro de Inicialização",
                f"Não foi possível carregar a lista de semestres: {str(e)}"
            )
