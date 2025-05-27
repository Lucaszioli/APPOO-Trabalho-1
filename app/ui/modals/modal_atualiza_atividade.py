from typing import Any, Optional, Callable
from app.ui.modals.modal_base import ModalBase
from app.models.atividade import Atividade
from app.services.service_universal import ServiceUniversal
from app.ui.components.date_picker import CTkDatePicker
from datetime import datetime
from CTkMessagebox import CTkMessagebox
import customtkinter

class ModalAtualizaAtividade(ModalBase):
    """Modal para atualização de uma atividade."""

    def __init__(
        self,
        disciplina: Any = None,
        conexao: Any = None,
        service: ServiceUniversal = None,
        master: Optional[Any] = None,
        callback: Optional[Callable] = None,
        item: Optional[Any] = None
    ):
        self.disciplina = disciplina  # Corrigido para não acessar item.disciplina
        self.item = item
        super().__init__(
            conexao=conexao,
            service=service,
            master=master,
            callback=callback,
            title="Editar Atividade",
            size=(600, 600),
            item=item
        )

    def _build_form(self) -> None:
        # Preenche os campos com os dados da atividade
        atividade = self.item
        self.add_field(
            key="nome",
            label="Nome da Atividade",
            required=True,
            placeholder="Ex: Prova Final"
        ).insert(0, getattr(atividade, "nome", ""))
        self.add_field(
            key="tipo",
            label="Tipo de Atividade",
            required=True,
            field_type="combobox",
            values=["Trabalho", "Prova", "Aula de campo", "Aula de revisão"]
        ).set(getattr(atividade, "tipo", ""))
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
        # Preenche a data
        data_val = getattr(atividade, "data", "")
        if data_val:
            try:
                if "/" in data_val:
                    day, month, year = map(int, data_val.split("/"))
                    data_iso = f"{year:04d}-{month:02d}-{day:02d}"
                else:
                    data_iso = data_val
                self.date_picker.insert(data_iso)
            except Exception:
                self.date_picker.insert(data_val)
        self.date_picker.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        self.add_field(
            key="pontuação",
            label="Pontuação Máxima",
            required=True,
            placeholder="Ex: 10",
            validator=lambda value: value.isdigit() and int(value) > 0
        ).insert(0, str(getattr(atividade, "pontuacao", getattr(atividade, "nota_total", ""))))
        self.add_field(
            key="observacao",
            label="Observações",
            field_type="textbox",
            required=False
        ).insert("1.0", getattr(atividade, "observacao", ""))

    def _validate_data(self, value: str) -> bool:
        try:
            day, month, year = map(int, value.split('/'))
            datetime(year, month, day)
        except ValueError:
            CTkMessagebox(title="Erro", message="Data inválida. Use o formato DD/MM/AAAA.", icon="cancel")
            return False
        return True

    def _validate_custom(self, data: dict) -> tuple[bool, str]:
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
        try:
            atividade = self.item
            atividade.nome = data["nome"]
            atividade.data = data["data"]
            atividade.tipo = data["tipo"]
            atividade.nota_total = int(data["pontuação"])
            atividade.pontuacao = int(data["pontuação"])
            atividade.observacao = data.get("observacao", "")
            # Garante atributos esperados pelo editar_bd
            for attr in ["disciplina_id", "nota", "lugar", "data_apresentacao"]:
                if not hasattr(atividade, attr):
                    setattr(atividade, attr, None)
            self.service.atividade_service.editar_bd(atividade)
            if self.callback:
                self.callback()
            self.destroy()
        except Exception as e:
            self.destroy()
            CTkMessagebox(title="Erro", message=f"Não foi possível atualizar a atividade: {str(e)}", icon="cancel")

    def _collect_data(self) -> dict:
        data = super()._collect_data()
        data["data"] = self.date_picker.get_date()
        return data
