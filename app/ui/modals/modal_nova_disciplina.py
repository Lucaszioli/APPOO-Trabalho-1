from typing import Any, Optional
from app.ui.modals.modal_base import ModalBase
from app.models.disciplinas import Disciplina
from app.services.service_universal import ServiceUniversal

class ModalNovaDisciplina(ModalBase):
    """Modal para criação de uma nova disciplina."""

    def __init__(
        self,
        semestre: Any,
        conexao: Any,
        service: ServiceUniversal,
        master: Optional[Any] = None,
        callback: Optional[callable] = None
    ) -> None:
        self.semestre = semestre
        super().__init__(
            conexao=conexao,
            service=service,
            master=master,
            callback=callback,
            title="Nova Disciplina",
            size=(600, 600),
        )

    def _build_form(self) -> None:
        self.add_field(
            key="nome",
            label="Nome da Disciplina",
            required=True,
            placeholder="Ex: Programação Orientada a Objetos"
        )
        self.add_field(
            key="codigo",
            label="Código",
            required=True,
            placeholder="Ex: INF001",
            validator=self._validate_codigo
        )
        self.add_field(
            key="carga",
            label="Carga Horária (horas)",
            required=True,
            placeholder="Ex: 60",
            validator=self._validate_carga_horaria
        )
        self.add_field(
            key="observacao",
            label="Observações",
            field_type="textbox",
            required=False
        )

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
        carga = int(data["carga"])
        self.disciplina = self.service.disciplina_service.criar_disciplina(
            nome=data["nome"],
            carga_horaria=carga,
            semestre=self.semestre,
            codigo=data["codigo"],
            observacao=data.get("observacao") or None
        )