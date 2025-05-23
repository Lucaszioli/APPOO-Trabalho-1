from datetime import datetime
from typing import Any, Optional
import customtkinter
from app.components.base_modal import BaseModal
from app.components.date_picker import CTkDatePicker
from app.services.service_universal import ServiceUniversal
class ModalAtualizaSemestre(BaseModal):
    """Modal para atualização de um semestre."""
    def __init__(
        self,
        conexao: Any,
        service: "ServiceUniversal",
        master: Optional[customtkinter.CTk] = None,
        callback: Optional[callable] = None,
        item: Optional[Any] = None
    ):
        self.item = item
        super().__init__(
            conexao=conexao,
            master=master,
            callback=callback,
            service=service,
            item=item,
            title="Editando Semestre: " + self.item.nome,
            size=(400, 300)
        )

    def _build_widgets(self) -> None:
        # Novo nome do semestre
        customtkinter.CTkLabel(self, text="Novo nome:").pack(pady=(20, 5))
        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.insert(0, self.item.nome)
        self.entry_nome.pack(fill="x", padx=20, pady=(0, 10))
        
        # Nova data de início
        customtkinter.CTkLabel(self, text="Nova data de início:").pack(pady=(0, 5))
        self.entry_inicio = CTkDatePicker(self)
        self.entry_inicio.insert(self.item.data_inicio)
        self.entry_inicio.set_date_format("%d/%m/%Y")
        self.entry_inicio.set_allow_manual_input(False)
        self.entry_inicio.pack(pady=(0, 10))
        
        # Nova data de fim
        customtkinter.CTkLabel(self, text="Nova data de fim:").pack(pady=(0, 5))
        self.entry_fim = CTkDatePicker(self)
        self.entry_fim.insert(self.item.data_fim)
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
            "nome": self.entry_nome.get().strip() if self.entry_nome.get().strip() else self.item.nome,
            "inicio": self.entry_inicio.get_date().strip() if self.entry_inicio.get_date().strip() else self.item.data_inicio,
            "fim": self.entry_fim.get_date().strip() if self.entry_fim.get_date().strip() else self.item.data_fim
        }
    
    def _validate(self, data: dict) -> tuple[bool, str]:
        return True, ""
    
    def _save(self, data: dict) -> None:
        # helper to parse either ISO or dd/mm/YYYY
        def _parse(raw):
            if isinstance(raw, str):
                try:
                    return datetime.fromisoformat(raw)
                except ValueError:
                    return datetime.strptime(raw, "%d/%m/%Y")
            return raw

        dt_inicio = _parse(data["inicio"])
        dt_fim    = _parse(data["fim"])

        # Update the model instance
        self.item.nome        = data["nome"]
        self.item.data_inicio = dt_inicio
        self.item.data_fim    = dt_fim

        # Persist the updated model
        self.service.semestre_service.editar_bd(self.item)