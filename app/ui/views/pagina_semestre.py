from app.ui.views.base_window import BaseWindow
from app.ui.listframes.listframe_disciplinas import DisciplinasFrame
from app.ui.listframes.listframe_atividades import AtividadesFrame
from app.ui.components.calendario_atividades import CalendarioAtividades
from typing import Any
import customtkinter

class PaginaSemestre(BaseWindow):
    """Janela de detalhes de um semestre específico."""
    def __init__(self, semestre: Any, conexao: Any, service: Any) -> None:
        self.semestre = semestre
        periodo = self._format_periodo(semestre)
        title = f"Semestre: {semestre.nome} {periodo}"
        super().__init__(
            conexao=conexao,
            title=title,
            service=service
        )

    def _format_periodo(self, semestre: Any) -> str:
        try:
            if hasattr(semestre, 'data_inicio') and hasattr(semestre, 'data_fim'):
                from datetime import datetime
                if isinstance(semestre.data_inicio, str):
                    inicio = datetime.strptime(semestre.data_inicio, "%Y-%m-%d")
                else:
                    inicio = semestre.data_inicio
                if isinstance(semestre.data_fim, str):
                    fim = datetime.strptime(semestre.data_fim, "%Y-%m-%d")
                else:
                    fim = semestre.data_fim
                return f"({inicio.strftime('%d/%m/%Y')} - {fim.strftime('%d/%m/%Y')})"
        except Exception:
            pass
        return ""

    def _create_body(self) -> None:
        try:
            self.disciplinas_frame = DisciplinasFrame(
                conexao=self.conexao,
                semestre=self.semestre,
                service=self.service,
                master=self
            )
            self.disciplinas_frame.configure(corner_radius=0)
            self.disciplinas_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        except Exception as e:
            self.show_error_message(
                "Erro de Inicialização",
                f"Não foi possível carregar as disciplinas do semestre: {str(e)}"
            )

    def show_frame(self, disciplina):
        if hasattr(self, 'disciplinas_frame') and self.disciplinas_frame:
            self.disciplinas_frame.destroy()
        elif hasattr(self, 'atividades_frame') and self.atividades_frame:
            self.atividades_frame.destroy()
            
        self.atividades_frame = AtividadesFrame(
            conexao=self.conexao,
            disciplina=disciplina,
            service=self.service,
            master=self
        )
        self.atividades_frame.configure(corner_radius=0)
        self.atividades_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
