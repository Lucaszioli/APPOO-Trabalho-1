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
            title="Editar Semestre: " + item.nome,
            size=(400, 300)
        )
        
    def _build_widgets(self) -> None:
        # Nome do semestre
        customtkinter.CTkLabel(self, text="Nome do Semestre:").pack(pady=(20, 5))
        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.pack(fill="x", padx=20, pady=(0, 10))

    def _collect_data(self) -> dict:
        return {
            "id": self.item.id,
            "nome": self.entry_nome.get().strip(),
        }
    
    def _validate(self, data: dict) -> tuple[bool, str]:
        if not data["nome"]:
            return False, "Nome do semestre não pode ser vazio."
        if len(data["nome"]) > 50:
            return False, "Nome do semestre deve ter no máximo 50 caracteres."
        return True, ""
    
    def _save(self, data: dict) -> None:
        semestre_service = SemestreService(self.conexao)
        semestre_service.atualiza_semestre(data["id"], data["nome"])