from typing import Any, Optional, Callable
from app.ui.modals.modal_base import ModalBase
from app.models.atividade import Atividade
from app.services.service_universal import ServiceUniversal
from datetime import datetime
from customtkinter import CTkMessagebox

class ModalNovaAtividade(ModalBase):
    """Modal para criação de uma nova atividade."""

    def __init__(
        self,
        disciplina: Any,
        conexao: Any,
        service: ServiceUniversal,
        master: Optional[Any] = None,
        callback: Optional[Callable] = None
    ) -> None:
        self.disciplina = disciplina
        super().__init__(
            conexao=conexao,
            service=service,
            master=master,
            callback=callback,
            title="Nova Atividade",
            size=(600, 600),
        )

    def _build_form(self) -> None:
        self.add_field(
            key="nome",
            label="Nome da Atividade",
            required=True,
            placeholder="Ex: Prova Final"
        )
        self.add_field(
            key="data",
            label="Data (DD/MM/AAAA)",
            required=True,
            placeholder="Ex: 15/12/2023",
            validator=self._validate_data
        )
        self.add_field(
            key="pontuação",
            label="Pontuação Máxima",
            required=True,
            placeholder="Ex: 10",
            validator=lambda value: value.isdigit() and int(value) > 0
        )
        
        self.add_field(
            key="observacao",
            label="Observações",
            field_type="textbox",
            required=False
        )

    def _validate_data(self, value: str) -> bool:
        """Valida se a data está no formato correto e é válida."""
        try:
            day, month, year = map(int, value.split('/'))
            datetime(year, month, day)  # Verifica se a data é válida
        except ValueError:
            CTkMessagebox(title="Erro", message="Data inválida. Use o formato DD/MM/AAAA.", icon="cancel")
            return False
        return True
    
    def _validate_custom(self, data: dict) -> tuple[bool, str]:
        """Valida campos personalizados antes de salvar."""
        if not data["nome"]:
            return False, "O nome da atividade é obrigatório."
        if not data["data"]:
            return False, "A data da atividade é obrigatória."
        if not data["pontuação"].isdigit() or int(data["pontuação"]) <= 0:
            return False, "A pontuação deve ser um número positivo."
        return True, ""
    
    def _save(self, data: dict) -> None:
        """Salva a nova atividade no banco de dados."""
        try:
            atividade = Atividade(
                nome=data["nome"],
                data=datetime.strptime(data["data"], "%d/%m/%Y"),
                pontuacao=int(data["pontuação"]),
                observacao=data.get("observacao", ""),
                disciplina_id=self.disciplina.id
            )
            self.service.save(atividade)
            if self.callback:
                self.callback(atividade)
            self.close()
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Não foi possível salvar a atividade: {str(e)}", icon="cancel")
        