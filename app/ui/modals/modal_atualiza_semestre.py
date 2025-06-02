from typing import Any, Optional
from datetime import datetime
from app.ui.modals.modal_base import ModalBase
from app.ui.components.date_picker import CTkDatePicker
from app.services.service_universal import ServiceUniversal
import customtkinter

class ModalAtualizaSemestre(ModalBase):
    """Modal melhorado para atualização de semestre."""
    
    def __init__(
        self,
        service: "ServiceUniversal",
        master: Optional[Any] = None,
        callback: Optional[callable] = None,
        item: Optional[Any] = None
    ):
        self.item = item
        super().__init__(
            service=service,
            master=master,
            callback=callback,
            title=f"Editando: {item.nome if item else 'Semestre'}",
            size=(500, 400),
            item=item
        )

    def _build_form(self) -> None:
        """Constrói o formulário de edição do semestre."""
        # Nome do semestre
        nome_field = self.add_field(
            key="nome",
            label="Nome do Semestre",
            required=True,
            placeholder="Ex: 2024.1, Outono 2024, etc."
        )
        if self.item:
            nome_field.insert(0, self.item.nome)
        
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
        
        inicio_placeholder = self._to_br_format(self.item.data_inicio) if self.item else "Ex: 01/01/2024"
        self.date_inicio = CTkDatePicker(dates_container, placeholder=inicio_placeholder)
        self.date_inicio.set_date_format("%d/%m/%Y")
        self.date_inicio.set_allow_manual_input(False)
        if self.item:
            self.date_inicio.insert(self._to_br_format(self.item.data_inicio))
        self.date_inicio.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        
        # Data de fim
        fim_label = customtkinter.CTkLabel(
            dates_container,
            text="Data de Fim*:",
            font=customtkinter.CTkFont(size=14)
        )
        fim_label.grid(row=0, column=1, sticky="w")
        
        fim_placeholder = self._to_br_format(self.item.data_fim) if self.item else "Ex: 30/06/2024"
        self.date_fim = CTkDatePicker(dates_container, placeholder=fim_placeholder)
        self.date_fim.set_date_format("%d/%m/%Y")
        self.date_fim.set_allow_manual_input(False)
        if self.item:
            self.date_fim.insert(self._to_br_format(self.item.data_fim))
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
            from datetime import datetime
            
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
                
        except (ValueError, TypeError) as e:  # Corrigido: captura mais específica
            return False, f"Formato de data inválido: {str(e)}"
            
        return True, ""

    def _save(self, data: dict) -> None:
        """Salva as alterações no semestre."""
        self.item.nome = data["nome"]
        self.item.data_inicio = data["data_inicio"]
        self.item.data_fim = data["data_fim"]
        
        self.service.semestre_service.editar_bd(self.item)

    def _to_iso(self, date_str):
        from datetime import datetime
        try:
            # Se já está no formato ISO
            datetime.fromisoformat(date_str)
            return date_str
        except ValueError:
            try:
                # Tenta converter do formato brasileiro
                return datetime.strptime(date_str, "%d/%m/%Y").date().isoformat()
            except Exception:
                return date_str

    def _to_br_format(self, date_str):
        from datetime import datetime
        try:
            # Se já está no formato brasileiro
            datetime.strptime(date_str, "%d/%m/%Y")
            return date_str
        except ValueError:
            try:
                # Se está no formato ISO
                return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
            except Exception:
                return date_str