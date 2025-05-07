# app/components/disciplinas_frame.py
import logging
from typing import Any

from app.components.base_list_frame import BaseListFrame
from app.services.disciplinas_services import DisciplinaServices
from app.components.modal_nova_disciplina import ModalNovaDisciplina

logger = logging.getLogger(__name__)


class DisciplinasFrame(BaseListFrame):
    """Frame para listar e gerenciar disciplinas."""

    def get_items(self, conexao: Any):
        """Retorna todas as disciplinas cadastradas."""
        return DisciplinaServices.listar_disciplinas(self.semestre, conexao)

    def modal_class(self):
        """Classe do modal usado para criar nova disciplina."""
        return ModalNovaDisciplina(self.semestre, self.conexao)

    def detail_view_class(self):
        """Classe da view de detalhe de disciplina."""
        print("Disciplina selecionada")
        return None

    def get_id(self, item: Any):
        """Extrai o identificador único da disciplina."""
        return getattr(item, "id", None)

    def item_name(self, item: Any):
        """Extrai o nome da disciplina para exibição no botão."""
        return getattr(item, "nome", "")

    def item_name_singular(self):
        return "disciplina"

    def item_name_plural(self):
        return "disciplinas"

    def title_text(self):
        return "Minhas Disciplinas"

    def subtitle_text(self):
        return "Selecione ou adicione uma disciplina:"

    def add_button_text(self):
        return "Adicionar Disciplina"
    
    def _on_add(self):
        """
        Abre o modal de nova disciplina com os argumentos corretos
        (semestre, conexão, master e callback).
        """
        try:
            ModalNovaDisciplina(
                semestre=self.semestre,
                conexao=self.conexao,
                master=self,
                callback=self._reload
            )
        except Exception as e:
            # opcional: mostrar caixa de erro
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(
                title="Erro",
                message=f"Não foi possível abrir o formulário de disciplina.\n{e}",
                icon="cancel"
            )
