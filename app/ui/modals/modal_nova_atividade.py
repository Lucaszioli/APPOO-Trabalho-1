from typing import Any, Optional, Callable
from app.ui.modals.modal_base import ModalBase
from app.models.atividade import Atividade
from app.services.service_universal import ServiceUniversal
from app.ui.components.date_picker import CTkDatePicker
from datetime import datetime
from CTkMessagebox import CTkMessagebox
import customtkinter

class ModalNovaAtividade(ModalBase):
    """Modal para criação de uma nova atividade."""

    def __init__(
        self,
        disciplina: Any,
        conexao: Any,
        service: ServiceUniversal,
        master: Optional[Any] = None,
        callback: Optional[Callable] = None
    ) -> None:
        self.disciplina = disciplina
        super().__init__(
            conexao=conexao,
            service=service,
            master=master,
            callback=callback,
            title="Nova Atividade",
            size=(600, 600),
        )

    def _build_form(self) -> None:
        self.add_field(
            key="nome",
            label="Nome da Atividade",
            required=True,
            placeholder="Ex: Prova Final"
        )
        # Adiciona seleção de tipo de atividade
        self.add_field(
            key="tipo",
            label="Tipo de Atividade",
            required=True,
            field_type="combobox",
            values=["Trabalho", "Prova", "Aula de campo", "Aula de revisão"]
        )
        dates_container = customtkinter.CTkFrame(self.form_frame, fg_color="transparent")
        dates_container.pack(fill="x", pady=10)
        dates_container.grid_columnconfigure((0, 1), weight=1)
        data_label = customtkinter.CTkLabel(
            dates_container,
            text="Data da Atividade*:",
            font=customtkinter.CTkFont(size=14)
        )
        data_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.date_picker = CTkDatePicker(dates_container)
        self.date_picker.set_date_format("%d/%m/%Y")
        self.date_picker.set_allow_manual_input(False)
        self.date_picker.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        self.add_field(
            key="pontuação",
            label="Pontuação Máxima",
            required=True,
            placeholder="Ex: 10",
            validator=lambda value: value.isdigit() and int(value) > 0
        )
        self.add_field(
            key="observacao",
            label="Observações",
            field_type="textbox",
            required=False
        )

    def _validate_data(self, value: str) -> bool:
        """Valida se a data está no formato correto e é válida."""
        try:
            day, month, year = map(int, value.split('/'))
            datetime(year, month, day)  # Verifica se a data é válida
        except ValueError:
            CTkMessagebox(title="Erro", message="Data inválida. Use o formato DD/MM/AAAA.", icon="cancel")
            return False
        return True
    
    def _validate_custom(self, data: dict) -> tuple[bool, str]:
        """Valida campos personalizados antes de salvar."""
        if not data["nome"]:
            return False, "O nome da atividade é obrigatório."
        if not data["data"]:
            return False, "A data da atividade é obrigatória."
        if not data["tipo"]:
            return False, "O tipo da atividade é obrigatório."
        if not data["pontuação"].isdigit() or int(data["pontuação"]) <= 0:
            return False, "A pontuação deve ser um número positivo."
        return True, ""
    
    def _save(self, data: dict) -> None:
        """Salva a nova atividade no banco de dados."""
        try:
            self.service.atividade_service.criar_atividade(
                nome=data["nome"],
                data=data["data"],
                disciplina=self.disciplina,
                tipo=data["tipo"],
                observacao=data.get("observacao", "")
            )
            if self.callback:
                self.callback()
            self.destroy()
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Não foi possível salvar a atividade: {str(e)}", icon="cancel")

    def _collect_data(self) -> dict:
        data = super()._collect_data()
        data["data"] = self.date_picker.get_date()
        return data
