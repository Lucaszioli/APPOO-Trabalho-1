from app.ui.listframes.listframe_base import ListFrameBase, ItemCard
from app.ui.components.components_base import StyledLabel
from app.ui.components.calendario_atividades import CalendarioAtividades
from app.services.atividade_services import AtividadeService
from typing import Any
import customtkinter

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
        
        if hasattr(self.item, 'tipo') and (self.item.tipo == "Trabalho" or self.item.tipo == "Prova"):
            pontuacao_label = StyledLabel(
                info_container,
                text=f"Pontuação: {self.item.nota_total} pontos",
                style='small'
            )
            pontuacao_label.grid(row=1, column=1, sticky="e")
            if hasattr(self.item, 'nota') and self.item.nota is not None:
                nota_label = StyledLabel(
                    info_container,
                    text=f"Nota: {self.item.nota} pontos",
                    style='small'
                )
                nota_label.grid(row=1, column=0, sticky="w", padx=(0, 10))
        if hasattr(self.item, 'progresso'):
            progresso_label = StyledLabel(
                info_container,
                text=f"Progresso: {self.item.progresso}",
                style='caption',
                wraplength=300
            )
            progresso_label.grid(row=2, column=0, sticky="w", padx=(0, 10))
        if hasattr(self.item, 'observacao') and self.item.observacao:
            obs_label = StyledLabel(
                parent,
                text=f"Observação: {self.item.observacao}",
                style='caption',
                wraplength=300
            )
            obs_label.pack(anchor="w", pady=(5, 0))
            
class AtividadesFrame(ListFrameBase):
    """Frame para listar e gerenciar atividades com calendário integrado."""

    def __init__(self, conexao, disciplina, service, master=None):
        self.disciplina = disciplina
        self.calendario = None
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
        from app.ui.modals.modal_atualiza_atividade import ModalAtualizaAtividade
        return ModalAtualizaAtividade
    
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
        return f"Disciplina: {self.disciplina.nome}"
    
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
            int(getattr(item, 'nota_total', 0) or 0) for item in self.items
        )
        return f"Total de atividades: {total_atividades} • Pontuação total distribuida: {total_pontuacao}"
    
    def _on_add(self):
        cls = self.modal_class_add()
        params = dict(conexao=self.conexao, service=self.service, master=self, callback=self._reload)
        params['disciplina'] = self.disciplina  # Corrige para passar a disciplina
        cls(**params)
    
    def _build_ui(self):
        """Constrói a interface melhorada com calendário."""
        # Criar container principal com duas colunas
        main_container = customtkinter.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        main_container.grid_columnconfigure(0, weight=1)  # Coluna do calendário
        main_container.grid_columnconfigure(1, weight=1)  # Coluna da lista
        main_container.grid_rowconfigure(0, weight=1)
        
        # Lado esquerdo: Calendário de atividades
        calendario_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        calendario_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.calendario = CalendarioAtividades(
            calendario_frame, 
            service=self.service, 
            disciplina=self.disciplina
        )
        self.calendario.pack(fill="both", expand=True)
        
        # Lado direito: Lista tradicional de atividades
        list_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Configurar o frame da lista como container
        self.list_main_container = list_frame
        
        # Criar componentes da lista no frame direito
        self._create_list_components()
        
    def _create_list_components(self):
        """Cria os componentes da lista de atividades."""
        # Cabeçalho da lista
        self._create_header_in_container(self.list_main_container)
        
        # Barra de busca
        self._create_search_bar_in_container(self.list_main_container)
        
        # Lista de itens
        self._create_items_list_in_container(self.list_main_container)
        
        # Rodapé
        self._create_footer_in_container(self.list_main_container)
        
    def _create_header_in_container(self, container):
        """Cria o cabeçalho no container especificado."""
        from app.ui.components.components_base import Card, StyledLabel, StyledButton
        
        header_card = Card(container, title="Lista de Atividades")
        header_card.pack(fill="x", padx=10, pady=(0, 10))
        
        # Título
        title_label = StyledLabel(
            header_card.content_frame,
            text=self.title_text(),
            style='title',
            text_color=("gray10", "white"),
        )
        title_label.pack(anchor="w", pady=5)
        
        # Subtítulo
        subtitle_label = StyledLabel(
            header_card.content_frame,
            text=self.subtitle_text(),
            style='normal',
            text_color=("gray40", "gray70")
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Botão adicionar
        add_button = StyledButton(
            header_card.content_frame,
            text=f"{self.add_button_text()}",
            style='success',
            command=self._on_add,
            height=40,
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        add_button.pack(pady=(10, 0), fill="x")
        
    def _create_search_bar_in_container(self, container):
        """Cria a barra de busca no container especificado."""
        from app.ui.components.components_base import Card
        
        search_card = Card(container, title="Buscar")
        search_card.pack(fill="x", padx=10, pady=(0, 10))
        
        self.search_entry = customtkinter.CTkEntry(
            search_card.content_frame,
            textvariable=self.search_var,
            placeholder_text=f"Buscar {self.item_name_plural()}...",
            height=35,
            corner_radius=8
        )
        self.search_entry.pack(fill="x", pady=5)
        
    def _create_items_list_in_container(self, container):
        """Cria a lista de itens no container especificado."""
        from app.ui.components.components_base import Card
        
        list_card = Card(container, title=f"{self.item_name_plural().title()}")
        list_card.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Container scrollável
        self.list_container = customtkinter.CTkScrollableFrame(
            list_card.content_frame,
            fg_color="transparent"
        )
        self.list_container.pack(fill="both", expand=True)
        
        self._populate_list()
        
    def _create_footer_in_container(self, container):
        """Cria o rodapé no container especificado."""
        from app.ui.components.components_base import Card, StyledLabel
        
        footer_card = Card(container)
        footer_card.pack(fill="x", padx=10, pady=(10, 0))
        footer_card.configure(border_width=1, border_color=("gray80", "gray20"))

        self.stats_label = StyledLabel(
            footer_card.content_frame,
            text=self._get_stats_text(),
            style='small', 
            text_color=("gray50", "gray60")
        )
        self.stats_label.pack()
        
    def _reload(self):
        """Recarrega itens e atualiza interface, incluindo o calendário."""
        super()._reload()
        if self.calendario:
            self.calendario.refresh()