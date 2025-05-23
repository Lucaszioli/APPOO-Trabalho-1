from datetime import datetime
from typing import Any, Optional
import customtkinter
from app.components.base_modal import BaseModal
from app.components.date_picker import CTkDatePicker
from app.services.service_universal import ServiceUniversal
class ModalAtualizaDisciplina(BaseModal):
    """Modal para atualização de uma disciplina."""
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
            title="Editando Disciplina: " + self.item.nome,
            size=(400, 380)
        )

    def _build_widgets(self) -> None:
        # Novo nome da disciplina
        customtkinter.CTkLabel(self, text="Nome da Disciplina:").pack(pady=(20, 5))
        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.insert(0, self.item.nome)
        self.entry_nome.pack(fill="x", padx=20, pady=(0, 10))

        # Nova carga horária
        customtkinter.CTkLabel(self, text="Carga Horária (h):").pack(pady=(0, 5))
        self.entry_carga = customtkinter.CTkEntry(self)
        self.entry_carga.insert(0, self.item.carga_horaria)
        self.entry_carga.pack(fill="x", padx=20, pady=(0, 10))

        # Novo código da disciplina
        customtkinter.CTkLabel(self, text="Código:").pack(pady=(0, 5))
        self.entry_codigo = customtkinter.CTkEntry(self)
        self.entry_codigo.insert(0, self.item.codigo)
        self.entry_codigo.pack(fill="x", padx=20, pady=(0, 10))

        # Nova observação (opcional)
        customtkinter.CTkLabel(self, text="Observação (opcional):").pack(pady=(0, 5))
        self.entry_observacao = customtkinter.CTkEntry(self)
        self.entry_observacao.insert(0, self.item.observacao)
        self.entry_observacao.pack(fill="x", padx=20, pady=(0, 20))

        # Botão salvar
        customtkinter.CTkButton(
            self,
            text="Salvar",
            command=self._on_submit
        ).pack()
      
    def _collect_data(self) -> dict:
        return {
            "nome": self.entry_nome.get().strip() if self.entry_nome.get().strip() else self.item.nome,
            "carga": self.entry_carga.get().strip() if self.entry_carga.get().strip() else self.item.carga_horaria,
            "codigo": self.entry_codigo.get().strip() if self.entry_codigo.get().strip() else self.item.codigo,
            "observacao": self.entry_observacao.get().strip() if self.entry_observacao.get().strip() else self.item.observacao,
            "id": self.item.id
        }
    
    def _validate(self, data: dict) -> tuple[bool, str]:
        return True, ""
    
    def _save(self, data: dict) -> None:
        self.item.nome = data["nome"]
        self.item.carga_horaria = data["carga"]
        self.item.codigo = data["codigo"]
        self.item.observacao = data["observacao"]
        
        self.service.disciplina_service.editar_bd(self.item)
        
        print(f"Disciplina atualizada: {self.item.semestre_id}")
