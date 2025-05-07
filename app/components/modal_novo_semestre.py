import logging
from datetime import datetime
from typing import Any, Callable, Optional
import customtkinter
from CTkMessagebox import CTkMessagebox
from app.components.date_picker import CTkDatePicker
from app.services.semestre_services import SemestreService
from app.errors.nomeSemestre import NomeRepetidoError

logger = logging.getLogger(__name__)

class ModalNovoSemestre(customtkinter.CTkToplevel):
    """Modal para adicionar um novo semestre ao sistema."""
    def __init__(
        self,
        conexao: Any,
        master: Optional[customtkinter.CTk] = None,
        callback: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(master)
        self.callback = callback
        if conexao is None:
            CTkMessagebox(title="Erro", message="Conexão não fornecida.", icon="cancel")
            self.destroy()
            return
        self.conexao = conexao
        self.title("Adicionar Novo Semestre")
        self.geometry("400x300")
        self._build_widgets()

    def _build_widgets(self) -> None:
        customtkinter.CTkLabel(self, text="Nome do Semestre:").pack(pady=(20, 5))
        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.pack(pady=(0, 10), fill="x", padx=20)

        customtkinter.CTkLabel(self, text="Data de Início:").pack(pady=(0, 5))
        self.entry_data_inicio = CTkDatePicker(self)
        self.entry_data_inicio.set_date_format("%d/%m/%Y")
        self.entry_data_inicio.set_allow_manual_input(False)
        self.entry_data_inicio.pack(pady=(0, 10))

        customtkinter.CTkLabel(self, text="Data de Fim:").pack(pady=(0, 5))
        self.entry_data_fim = CTkDatePicker(self)
        self.entry_data_fim.set_date_format("%d/%m/%Y")
        self.entry_data_fim.set_allow_manual_input(False)
        self.entry_data_fim.pack(pady=(0, 20))

        customtkinter.CTkButton(
            self,
            text="Adicionar",
            command=self._on_submit
        ).pack()

    def _on_submit(self) -> None:
        nome = self.entry_nome.get().strip()
        inicio_str = self.entry_data_inicio.get_date()
        fim_str = self.entry_data_fim.get_date()

        if not nome or not inicio_str or not fim_str:
            CTkMessagebox(title="Erro", message="Todos os campos são obrigatórios.", icon="cancel")
            return

        try:
            inicio = datetime.strptime(inicio_str, "%d/%m/%Y")
            fim = datetime.strptime(fim_str, "%d/%m/%Y")
        except ValueError:
            CTkMessagebox(title="Erro", message="Formato de data inválido.", icon="cancel")
            return

        if inicio > fim:
            CTkMessagebox(title="Erro", message="Data de início deve ser antes da data de fim.", icon="cancel")
            return

        try:
            SemestreService.criar(
                nome,
                inicio.strftime("%Y-%m-%d"),
                fim.strftime("%Y-%m-%d"),
                self.conexao
            )
        except NomeRepetidoError as e:
            CTkMessagebox(title="Erro", message=str(e), icon="cancel")
            return
        except Exception:
            logger.exception("Falha ao criar semestre")
            CTkMessagebox(title="Erro", message="Erro ao salvar semestre.", icon="cancel")
            return

        if self.callback:
            try:
                self.callback()
            except Exception:
                logger.warning("Callback de atualização falhou")
        self.destroy()