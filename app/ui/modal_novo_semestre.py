from typing import Any, Optional
from datetime import datetime
from app.ui.modal_base import ModalBase
from app.ui.components.date_picker import CTkDatePicker
from app.services.service_universal import ServiceUniversal
import customtkinter

class ModalNovoSemestre(ModalBase):
    """Modal melhorado para criação de novo semestre."""
    
    def __init__(
        self,
        conexao: Any,
        service: "ServiceUniversal",
        master: Optional[Any] = None,
        callback: Optional[callable] = None,
    ):
        super().__init__(
            conexao=conexao,
            service=service,
            master=master,
            callback=callback,
            title="Novo Semestre",
            size=(500, 400),
        )

    def _build_form(self) -> None:
        """Constrói o formulário de novo semestre."""
        # Nome do semestre
        self.add_field(
            key="nome",
            label="Nome do Semestre",
            required=True,
            placeholder="Ex: 2024.1, Outono 2024, etc."
        )
        
        # Container para datas
        dates_container = customtkinter.CTkFrame(self.form_frame, fg_color="transparent")
        dates_container.pack(fill="x", pady=10)
        dates_container.grid_columnconfigure((0, 1), weight=1)
        
        # Data de início
        inicio_label = customtkinter.CTkLabel(
            dates_container,
            text="Data de Início*:",
            font=customtkinter.CTkFont(size=14)
        )
        inicio_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.date_inicio = CTkDatePicker(dates_container)
        self.date_inicio.set_date_format("%d/%m/%Y")
        self.date_inicio.set_allow_manual_input(False)
        self.date_inicio.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        
        # Data de fim
        fim_label = customtkinter.CTkLabel(
            dates_container,
            text="Data de Fim*:",
            font=customtkinter.CTkFont(size=14)
        )
        fim_label.grid(row=0, column=1, sticky="w")
        
        self.date_fim = CTkDatePicker(dates_container)
        self.date_fim.set_date_format("%d/%m/%Y")
        self.date_fim.set_allow_manual_input(False)
        self.date_fim.grid(row=1, column=1, sticky="ew")
        
    def _collect_data(self) -> dict:
        """Coleta dados do formulário incluindo datas."""
        data = super()._collect_data()
        data["data_inicio"] = self.date_inicio.get_date()
        data["data_fim"] = self.date_fim.get_date()
        return data
        
    def _validate_custom(self, data: dict) -> tuple[bool, str]:
        """Validação customizada para semestre."""
        if not data["nome"]:
            return False, "Nome do semestre é obrigatório."
            
        if not data.get("data_inicio"):
            return False, "Data de início é obrigatória."
            
        if not data.get("data_fim"):
            return False, "Data de fim é obrigatória."
            
        # Validar se data de fim é posterior à data de início
        try:
            if isinstance(data["data_inicio"], str):
                inicio = datetime.strptime(data["data_inicio"], "%d/%m/%Y")
            else:
                inicio = data["data_inicio"]
                
            if isinstance(data["data_fim"], str):
                fim = datetime.strptime(data["data_fim"], "%d/%m/%Y")
            else:
                fim = data["data_fim"]
                
            if fim <= inicio:
                return False, "Data de fim deve ser posterior à data de início."
                
        except ValueError:
            return False, "Formato de data inválido."
            
        return True, ""

    def _save(self, data: dict) -> None:
        """Salva o novo semestre."""
        self.service.semestre_service.criar_semestre(
            nome=data["nome"],
            data_inicio=data["data_inicio"],
            data_fim=data["data_fim"]
        )