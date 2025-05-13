from datetime import datetime
from typing import Any, Optional
import customtkinter
from app.components.base_modal import BaseModal
from app.components.date_picker import CTkDatePicker
from app.services.semestre_services import SemestreService

class ModalAtualizaSemestre(BaseModal):
    """Modal para criação de um novo semestre."""
    def __init__(
        self,
        conexao: Any,
        master: Optional[customtkinter.CTk] = None,
        callback: Optional[callable] = None,
        item: Optional[Any] = None
    ):
        super().__init__(
            conexao=conexao,
            master=master,
            callback=callback,
            item=item,
            title="Editando Semestre: " + item.nome,
            size=(400, 300)
        )
        
    def _build_widgets(self) -> None:
        # Novo nome do semestre
        customtkinter.CTkLabel(self, text="Novo nome:").pack(pady=(20, 5))
        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.pack(fill="x", padx=20, pady=(0, 10))
        
        # Nova data de início
        customtkinter.CTkLabel(self, text="Nova data de início:").pack(pady=(0, 5))
        self.entry_inicio = CTkDatePicker(self)
        self.entry_inicio.set_date_format("%d/%m/%Y")
        self.entry_inicio.set_allow_manual_input(False)
        self.entry_inicio.pack(pady=(0, 10))
        
        # Nova data de fim
        customtkinter.CTkLabel(self, text="Nova data de fim:").pack(pady=(0, 5))
        self.entry_fim = CTkDatePicker(self)
        self.entry_fim.set_date_format("%d/%m/%Y")
        self.entry_fim.set_allow_manual_input(False)
        self.entry_fim.pack(pady=(0, 20))

    def _collect_data(self) -> dict:
        return None
    
    def _validate(self, data: dict) -> tuple[bool, str]:
        return True, ""
    
    def _save(self, data: dict) -> None:
        return None