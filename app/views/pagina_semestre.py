from app.views.base_window import BaseWindow
from app.ui.listframes.listframe_disciplinas import DisciplinasFrame

class PaginaSemestre(BaseWindow):
    """Janela melhorada de detalhes de um semestre específico."""

    def __init__(self, semestre, conexao, service):
        self.semestre = semestre
        
        # Formatação do título com informações do semestre
        periodo = self._format_periodo(semestre)
        title = f"{semestre.nome} {periodo}"
        
        super().__init__(
            conexao=conexao,
            title=title,
            service=service
        )

    def _format_periodo(self, semestre):
        """Formata período do semestre para o título."""
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
        """Cria o corpo principal com frame de disciplinas."""
        try:
            # Frame de disciplinas do semestre
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
