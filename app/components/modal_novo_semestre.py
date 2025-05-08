from datetime import datetime
from typing import Any, Optional
import customtkinter
from app.components.base_modal import BaseModal
from app.components.date_picker import CTkDatePicker
from app.services.semestre_services import SemestreService
from CTkMessagebox import CTkMessagebox

class ModalNovoSemestre(BaseModal):
    """Modal para criação de um novo semestre."""
    def __init__(
        self,
        conexao: Any,
        master: Optional[customtkinter.CTk] = None,
        callback: Optional[callable] = None
    ):
        super().__init__(
            conexao=conexao,
            master=master,
            callback=callback,
            title="Adicionar Novo Semestre",
            size=(400, 300)
        )

    def _build_widgets(self) -> None:
        # Nome do semestre
        customtkinter.CTkLabel(self, text="Nome do Semestre:").pack(pady=(20, 5))
        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.pack(fill="x", padx=20, pady=(0, 10))

        # Data de início 
        customtkinter.CTkLabel(self, text="Data de Início:").pack(pady=(0, 5))
        self.entry_inicio = CTkDatePicker(self)
        self.entry_inicio.set_date_format("%d/%m/%Y")
        self.entry_inicio.set_allow_manual_input(False)
        self.entry_inicio.pack(pady=(0, 10))

        # Data de fim
        customtkinter.CTkLabel(self, text="Data de Fim:").pack(pady=(0, 5))
        self.entry_fim = CTkDatePicker(self)
        self.entry_fim.set_date_format("%d/%m/%Y")
        self.entry_fim.set_allow_manual_input(False)
        self.entry_fim.pack(pady=(0, 20))

        # Botão salvar
        customtkinter.CTkButton(
            self,
            text="Salvar",
            command=self._on_submit
        ).pack()

    def _collect_data(self) -> dict:
        return {
            "nome": self.entry_nome.get().strip(),
            "inicio": self.entry_inicio.get_date().strip(),
            "fim": self.entry_fim.get_date().strip()
        }

    def _validate(self, data: dict) -> tuple[bool, str]:
        if not data["nome"]:
            return False, "Nome do semestre não pode ser vazio."
        try:
            dt_inicio = datetime.strptime(data["inicio"], "%d/%m/%Y")
            dt_fim = datetime.strptime(data["fim"], "%d/%m/%Y")
        except ValueError:
            return False, "Formato de data inválido. Use dd/mm/aaaa."
        if dt_inicio > dt_fim:
            return False, "Data de início deve ser anterior à data de fim."
        return True, ""

    def _save(self, data: dict) -> None:
        dt_inicio = datetime.strptime(data["inicio"], "%d/%m/%Y")
        dt_fim = datetime.strptime(data["fim"], "%d/%m/%Y")
        semestre = SemestreService.criar(
            nome=data["nome"],
            data_inicio=dt_inicio,
            data_fim=dt_fim,
            conexao = self.conexao
        )