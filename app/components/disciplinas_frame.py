# app/components/disciplinas_frame.py
import logging
from typing import Any
from app.components.improved_list_frame import ImprovedListFrame, ItemCard
from app.components.ui.base_components import StyledLabel
import customtkinter

from app.components.base_list_frame import BaseListFrame
from app.services.disciplinas_services import DisciplinaService

logger = logging.getLogger(__name__)


class DisciplinaCard(ItemCard):
    """Card específico para disciplinas."""
    
    def _add_item_info(self, parent):
        """Adiciona informações específicas da disciplina."""
        info_container = customtkinter.CTkFrame(parent, fg_color="transparent")
        info_container.pack(fill="x")
        info_container.grid_columnconfigure((0, 1), weight=1)
        
        # Código
        codigo_label = StyledLabel(
            info_container,
            text=f"Código: {self.item.codigo}",
            style='small'
        )
        codigo_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Carga horária
        carga_label = StyledLabel(
            info_container,
            text=f"{self.item.carga_horaria}h",
            style='small'
        )
        carga_label.grid(row=0, column=1, sticky="e")
        
        # Observação (se houver)
        if hasattr(self.item, 'observacao') and self.item.observacao:
            obs_label = StyledLabel(
                parent,
                text=f"{self.item.observacao}",
                style='caption',
                wraplength=300
            )
            obs_label.pack(anchor="w", pady=(5, 0))

class DisciplinasFrame(ImprovedListFrame):
    """Frame para listar e gerenciar disciplinas com design melhorado."""

    def get_items(self, conexao: Any):
        """Retorna todas as disciplinas cadastradas."""
        return self.service.disciplina_service.listar_por_semestre(self.semestre)

    def modal_class_add(self):
        """Classe do modal usado para criar nova disciplina."""
        from app.components.modal_nova_disciplina import ModalNovaDisciplina
        return ModalNovaDisciplina
    
    def modal_class_update(self):
        from app.components.modal_atualiza_disciplina import ModalAtualizaDisciplina
        return ModalAtualizaDisciplina

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
        return f"Disciplinas - {self.semestre.nome if self.semestre else 'Todas'}"

    def subtitle_text(self):
        return "Gerencie suas disciplinas de forma organizada"

    def add_button_text(self):
        return "Nova Disciplina"

    def delete_item(self, item):
        """Deleta uma disciplina."""
        return self.service.disciplina_service.deletar(item)

    def update_item(self, item):
        """Atualiza uma disciplina e recarrega a lista."""
        self.service.disciplina_service.editar_bd(item)
        self._load_items()
        self._populate_list()
        
    def _create_item_card(self, item):
        """Cria card customizado para disciplina."""
        return DisciplinaCard(self.list_container, item, self)
        
    def _get_stats_text(self):
        """Retorna estatísticas específicas das disciplinas."""
        total = len(self.items)
        total_horas = sum(int(getattr(item, 'carga_horaria', 0) or 0) for item in self.items)
        return f"Total: {total} disciplinas • {total_horas} horas"