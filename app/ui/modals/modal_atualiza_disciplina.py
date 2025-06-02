from datetime import datetime
from typing import Any, Optional
from app.ui.modals.modal_base import ModalBase
from app.services.service_universal import ServiceUniversal

class ModalAtualizaDisciplina(ModalBase):
    """Modal para atualização de disciplina."""

    def __init__(
        self,
        service: ServiceUniversal,
        master: Optional[Any] = None,
        callback: Optional[callable] = None,
        item: Optional[Any] = None
    ) -> None:
        self.item = item
        super().__init__(
            service=service,
            master=master,
            callback=callback,
            title=f"Editando: {item.nome if item else 'Disciplina'}",
            size=(600, 600),
            item=item
        )

    def _build_form(self) -> None:
        nome_field = self.add_field(
            key="nome",
            label="Nome da Disciplina",
            required=True,
            placeholder="Ex: Programação Orientada a Objetos"
        )
        if self.item:
            nome_field.insert(0, self.item.nome)
        codigo_field = self.add_field(
            key="codigo",
            label="Código",
            required=True,
            placeholder="Ex: INF001",
            validator=self._validate_codigo
        )
        if self.item:
            codigo_field.insert(0, self.item.codigo)
        carga_field = self.add_field(
            key="carga",
            label="Carga Horária (horas)",
            required=True,
            placeholder="Ex: 60",
            validator=self._validate_carga_horaria
        )
        if self.item:
            carga_field.insert(0, str(self.item.carga_horaria))
        obs_field = self.add_field(
            key="observacao",
            label="Observações",
            field_type="textbox",
            required=False
        )
        if self.item and self.item.observacao:
            obs_field.insert("1.0", self.item.observacao)

    def _validate_codigo(self, value: str) -> bool:
        return len(value) >= 3 and value.replace(" ", "").isalnum()

    def _validate_carga_horaria(self, value: str) -> bool:
        try:
            carga = int(value)
            return 1 <= carga <= 500
        except ValueError:
            return False

    def _validate_custom(self, data: dict) -> tuple[bool, str]:
        if not data["nome"]:
            return False, "Nome da disciplina é obrigatório."
        try:
            carga = int(data["carga"])
            if carga <= 0:
                return False, "Carga horária deve ser um número positivo."
        except ValueError:
            return False, "Carga horária deve ser um número válido."
        if not data["codigo"]:
            return False, "Código da disciplina é obrigatório."
        return True, ""

    def _save(self, data: dict) -> None:
        self.item.nome = data["nome"]
        self.item.carga_horaria = int(data["carga"])
        self.item.codigo = str(data["codigo"]).strip()
        self.item.observacao = data.get("observacao") or None
        self.service.disciplina_service.editar_bd(self.item)
