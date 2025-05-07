from typing import Any, Optional
import customtkinter
from app.components.base_modal import BaseModal
from app.models.disciplinas import Disciplina
from CTkMessagebox import CTkMessagebox

class ModalNovaDisciplina(BaseModal):
    """Modal para criação de uma nova disciplina."""
    def __init__(
        self,
        semestre: Any,
        conexao: Any,
        master: Optional[customtkinter.CTk] = None,
        callback: Optional[callable] = None
    ):
        super().__init__(
            conexao=conexao,
            master=master,
            callback=callback,
            title="Adicionar Nova Disciplina",
            size=(400, 280),
        )
        self.semestre = semestre

    def _build_widgets(self) -> None:
        # Nome da disciplina
        customtkinter.CTkLabel(self, text="Nome da Disciplina:").pack(pady=(20, 5))
        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.pack(fill="x", padx=20, pady=(0, 10))

        # Carga horária
        customtkinter.CTkLabel(self, text="Carga Horária (h):").pack(pady=(0, 5))
        self.entry_carga = customtkinter.CTkEntry(self)
        self.entry_carga.pack(fill="x", padx=20, pady=(0, 10))

        # Código da disciplina
        customtkinter.CTkLabel(self, text="Código:").pack(pady=(0, 5))
        self.entry_codigo = customtkinter.CTkEntry(self)
        self.entry_codigo.pack(fill="x", padx=20, pady=(0, 10))

        # Observação (opcional)
        customtkinter.CTkLabel(self, text="Observação (opcional):").pack(pady=(0, 5))
        self.entry_observacao = customtkinter.CTkEntry(self)
        self.entry_observacao.pack(fill="x", padx=20, pady=(0, 20))

        # Botão salvar
        customtkinter.CTkButton(
            self,
            text="Salvar",
            command=self._on_submit
        ).pack()

    def _collect_data(self) -> dict:
        return {
            "nome": self.entry_nome.get().strip(),
            "carga": self.entry_carga.get().strip(),
            "codigo": self.entry_codigo.get().strip(),
            "observacao": self.entry_observacao.get().strip() or None
        }

    def _validate(self, data: dict) -> tuple[bool, str]:
        if not data["nome"]:
            return False, "Nome da disciplina não pode ser vazio."
        try:
            carga = int(data["carga"])
            if carga <= 0:
                raise ValueError
        except ValueError:
            return False, "Carga horária deve ser um inteiro positivo."
        if not data["codigo"]:
            return False, "Código da disciplina não pode ser vazio."
        return True, ""

    def _save(self, data: dict) -> None:
        carga = int(data["carga"])
        disciplina = Disciplina(
            nome=data["nome"],
            carga_horaria=carga,
            semestre_id=self.semestre.id,
            codigo=data["codigo"],
            observacao=data.get("observacao")
        )
        disciplina.adicionar_bd(self.conexao)