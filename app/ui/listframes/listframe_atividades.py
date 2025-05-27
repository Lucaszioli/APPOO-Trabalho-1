from app.ui.listframes.listframe_base import ListFrameBase, ItemCard
from app.ui.components.components_base import StyledLabel
from app.services.atividade_services import AtividadeService
from typing import Any

class AtividadeCard(ItemCard):
    """Card para exibir informações de uma atividade."""
    
    def _add_item_info(self, parent):
        info_container = parent
        info_container.grid_columnconfigure((0, 1), weight=1)
        
        nome_label = StyledLabel(
            info_container,
            text=f"Nome: {self.item.nome}",
            style='small'
        )
        nome_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        data_label = StyledLabel(
            info_container,
            text=f"Data: {self.item.data}",
            style='small'
        )
        data_label.grid(row=0, column=1, sticky="e")
        
        if hasattr(self.item, 'observacao') and self.item.observacao:
            obs_label = StyledLabel(
                parent,
                text=f"Observação: {self.item.observacao}",
                style='caption',
                wraplength=300
            )
            obs_label.pack(anchor="w", pady=(5, 0))
            
class AtividadesFrame(ListFrameBase):
    """Frame para listar e gerenciar atividades."""

    def __init__(self, conexao, disciplina, service, master=None):
        self.disciplina = disciplina
        super().__init__(conexao=conexao, semestre=None, service=service, master=master)

    def get_items(self, conexao: Any) -> list:
        """Retorna todas as atividades cadastradas."""
        return self.service.atividade_service.listar_por_disciplina(self.disciplina)

    def modal_class_add(self) -> type:
        """Classe do modal usado para criar nova atividade."""
        from app.ui.modals.modal_nova_atividade import ModalNovaAtividade
        return ModalNovaAtividade
    
    def modal_class_update(self) -> type:
        """Classe do modal usado para atualizar atividade."""
        # from app.ui.modals.modal_atualiza_atividade import ModalAtualizaAtividade
        return True
    
    def detail_view_class(self):
        return True
    
    def get_id(self, item):
        """Retorna o ID da atividade."""
        return super().get_id(item)
    
    def item_name(self, item):
        return getattr(item, 'nome', 'Atividade Desconhecida')
    
    def item_name_singular(self):
        return "atividade"
    
    def item_name_plural(self):
        return "atividades"
    
    def title_text(self):
        return f"Atividades de {self.disciplina.nome}"
    
    def subtitle_text(self):
        return "Gerencie as atividades desta disciplina"
    
    def add_button_text(self):
        return "Nova Atividade"
    
    def delete_item(self, item):
        return self.service.atividade_service.deletar(item)
    
    def update_item(self, item):
        self.service.atividade_service.editar_bd(item)
        self._load_items()
        self._populate_list()
        
    def _create_item_card(self, item):
        return AtividadeCard(
            self.list_container,  # master
            item,
            self  # list_frame
        )
        
    def _get_stats_text(self):
        total_atividades = len(self.items)
        if total_atividades == 0:
            return "Nenhuma atividade cadastrada"
        total_pontuacao = sum(
            int(getattr(item, 'pontuacao', 0) or 0) for item in self.items
        )
        return f"Total de atividades: {total_atividades} • Pontuação total distribuida: {total_pontuacao}"
    
    def _on_add(self):
        cls = self.modal_class_add()
        params = dict(conexao=self.conexao, service=self.service, master=self, callback=self._reload)
        params['disciplina'] = self.disciplina  # Corrige para passar a disciplina
        cls(**params)