import logging
from typing import Any
from app.ui.listframes.listframe_base import ListFrameBase, ItemCard
from app.ui.components.components_base import StyledLabel
from app.ui.components.calendario_atividades import CalendarioAtividades
from app.services.disciplinas_services import DisciplinaService

import customtkinter


logger = logging.getLogger(__name__)

class DisciplinaCard(ItemCard):
    """Card para exibir informações de uma disciplina."""
    def _add_item_info(self, parent: Any) -> None:
        info_container = customtkinter.CTkFrame(parent, fg_color="transparent")
        info_container.pack(fill="x")
        info_container.grid_columnconfigure((0, 1), weight=1)
        
        codigo_label = StyledLabel(
            info_container,
            text=f"Código: {self.item.codigo}",
            style='small'
        )
        codigo_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        carga_label = StyledLabel(
            info_container,
            text=f"{self.item.carga_horaria}h",
            style='small'
        )
        carga_label.grid(row=0, column=1, sticky="e")
        
        if hasattr(self.item, 'observacao') and self.item.observacao:
            obs_label = StyledLabel(
                parent,
                text=f"{self.item.observacao}",
                style='caption',
                wraplength=300
            )
            obs_label.pack(anchor="w", pady=(5, 0))

class DisciplinasFrame(ListFrameBase):
    """Frame para listar e gerenciar disciplinas com calendário integrado."""
    
    def __init__(self, conexao, semestre, service, master=None):
        self.calendario = None
        super().__init__(conexao=conexao, semestre=semestre, service=service, master=master)

    def get_items(self, conexao: Any) -> list:
        """Retorna todas as disciplinas cadastradas."""
        return self.service.disciplina_service.listar_por_semestre(self.semestre)

    def modal_class_add(self) -> type:
        """Classe do modal usado para criar nova disciplina."""
        from app.ui.modals.modal_nova_disciplina import ModalNovaDisciplina
        return ModalNovaDisciplina
    
    def modal_class_update(self) -> type:
        from app.ui.modals.modal_atualiza_disciplina import ModalAtualizaDisciplina
        return ModalAtualizaDisciplina

    def detail_view_class(self):
        """Classe da view de detalhe de disciplina."""
        from app.ui.views.pagina_disciplina import PaginaDisciplina
        return PaginaDisciplina

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
        return f"Semestre: {self.semestre.nome if self.semestre else 'Todas'}"

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
        
    def _build_ui(self):
        """Constrói a interface melhorada com calendário."""
        main_container = customtkinter.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        main_container.grid_columnconfigure(0, weight=1)  
        main_container.grid_columnconfigure(1, weight=1)  
        main_container.grid_rowconfigure(0, weight=1)
        
        calendario_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        calendario_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.calendario = CalendarioAtividades(
            calendario_frame, 
            service=self.service, 
            semestre=self.semestre
        )
        self.calendario.pack(fill="both", expand=True)
        
        list_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.list_main_container = list_frame
        
        self._create_list_components()
        
    def _create_list_components(self):
        """Cria os componentes da lista de disciplinas."""
        self._create_header_in_container(self.list_main_container)
        
        self._create_search_bar_in_container(self.list_main_container)
        
        self._create_items_list_in_container(self.list_main_container)
        
        self._create_footer_in_container(self.list_main_container)
        
    def _create_header_in_container(self, container):
        """Cria o cabeçalho no container especificado."""
        from app.ui.components.components_base import Card, StyledLabel, StyledButton
        
        header_card = Card(container, title="Lista de Disciplinas")
        header_card.pack(fill="x", padx=10, pady=(0, 10))
        
        title_label = StyledLabel(
            header_card.content_frame,
            text=self.title_text(),
            style='title',
            text_color=("gray10", "white"),
        )
        title_label.pack(anchor="w", pady=5)
        
        subtitle_label = StyledLabel(
            header_card.content_frame,
            text=self.subtitle_text(),
            style='normal',
            text_color=("gray40", "gray70")
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
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