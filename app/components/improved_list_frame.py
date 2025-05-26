from abc import ABC, abstractmethod
import logging
import customtkinter
from CTkMessagebox import CTkMessagebox
from app.services.service_universal import ServiceUniversal
from app.components.ui.base_components import BaseComponent, StyledButton, StyledLabel, Card
import inspect

logger = logging.getLogger(__name__)

class ItemCard(Card):
    """Card para exibir um item da lista."""
    
    def __init__(self, master, item, list_frame, **kwargs):
        self.item = item
        self.list_frame = list_frame
        super().__init__(master, **kwargs)
        
    def _build_ui(self):
        super()._build_ui()
        
        # Container principal com grid
        main_container = customtkinter.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(fill="x", pady=5)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Nome do item (clicável)
        name_button = StyledButton(
            main_container,
            text=self.list_frame.item_name(self.item),
            style='secondary',
            command=lambda: self.list_frame._on_select(self.item),
            anchor="w",
            height=40,
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        name_button.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        # Informações adicionais
        info_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        info_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        self._add_item_info(info_frame)
        
        # Botões de ação
        actions_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        actions_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
        actions_frame.grid_columnconfigure(0, weight=1)
        
        # Botão editar
        edit_btn = StyledButton(
            actions_frame,
            text="Editar",
            style='primary',
            command=lambda: self.list_frame._on_update(self.item),
            width=80,
            height=30
        )
        edit_btn.grid(row=0, column=0, padx=(0, 5), sticky="e")
        
        # Botão excluir
        delete_btn = StyledButton(
            actions_frame,
            text="Excluir",
            style='danger',
            command=lambda: self.list_frame._on_delete(self.item),
            width=80,
            height=30
        )
        delete_btn.grid(row=0, column=1, sticky="e")
        
    def _add_item_info(self, parent):
        """Adiciona informações específicas do item. Pode ser sobrescrito."""
        pass

class ImprovedListFrame(BaseComponent, ABC):
    """Frame de lista melhorado com design moderno."""
    
    def __init__(self, conexao, semestre, service: "ServiceUniversal", master=None):
        if conexao is None:
            raise ValueError("Conexão não pode ser nula.")
        self.conexao = conexao
        self.semestre = semestre
        self.service = service
        self.items = []
        self.item_views = {}
        self.search_var = customtkinter.StringVar()
        self.search_var.trace('w', self._on_search)
        
        super().__init__(master)
        self._load_items()
        self._populate_list()  # Garante que a lista aparece ao abrir
        
    def _setup_style(self):
        super()._setup_style()
        self.configure(fg_color="transparent")
        
    def _build_ui(self):
        """Constrói a interface melhorada."""
        # Cabeçalho
        self._create_header()
        
        # Barra de busca e filtros
        self._create_search_bar()
        
        # Lista de itens
        self._create_items_list()
        
        # Rodapé com estatísticas
        self._create_footer()
        
    def _create_header(self):
        """Cria o cabeçalho da página."""
        header_card = Card(self)
        header_card.pack(fill="x", padx=20, pady=(0, 10))
        header_card.configure(border_width=1, border_color=("gray80", "gray20"))

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
     
    def _create_search_bar(self):
        """Cria a barra de busca."""
        search_card = Card(self, title="Buscar")
        search_card.pack(fill="x", padx=20, pady=(0, 10))
        
        self.search_entry = customtkinter.CTkEntry(
            search_card.content_frame,
            textvariable=self.search_var,
            placeholder_text=f"Buscar {self.item_name_plural()}...",
            height=35,
            corner_radius=8
        )
        self.search_entry.pack(fill="x", pady=5)
        
    def _create_items_list(self):
        """Cria a lista de itens."""
        list_card = Card(self, title=f"{self.item_name_plural().title()}")
        list_card.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Container scrollável
        self.list_container = customtkinter.CTkScrollableFrame(
            list_card.content_frame,
            fg_color="transparent"
        )
        self.list_container.pack(fill="both", expand=True)
        
        self._populate_list()
        
    def _create_footer(self):
        """Cria o rodapé com estatísticas."""
        footer_card = Card(self)
        footer_card.pack(fill="x", padx=20, pady=(10, 0))
        footer_card.configure(border_width=1, border_color=("gray80", "gray20"))

        self.stats_label = StyledLabel(
            footer_card.content_frame,
            text=self._get_stats_text(),
            style='small', 
            text_color=("gray50", "gray60")
        )
        self.stats_label.pack()
        
    def _get_stats_text(self):
        """Retorna texto com estatísticas."""
        total = len(self.items)
        return f"Total de {self.item_name_plural()}: {total}"
        
    def _on_search(self, *args):
        """Filtra itens baseado na busca."""
        self._populate_list()
        
    def _get_filtered_items(self):
        """Retorna itens filtrados pela busca."""
        search_term = self.search_var.get().lower()
        if not search_term:
            return self.items
            
        return [
            item for item in self.items 
            if search_term in self.item_name(item).lower()
        ]
        
    def _populate_list(self):
        """Popula a lista com cards dos itens."""
        # Limpa lista atual
        for widget in self.list_container.winfo_children():
            widget.destroy()
            
        filtered_items = self._get_filtered_items()
        
        if not filtered_items:
            empty_label = StyledLabel(
                self.list_container,
                text=f"Nenhum {self.item_name_singular()} encontrado.",
                style='caption'
            )
            empty_label.pack(pady=20)
            return
            
        # Cria cards para cada item
        for item in filtered_items:
            item_card = self._create_item_card(item)
            item_card.pack(fill="x", pady=5)
            
        # Atualiza estatísticas
        if hasattr(self, 'stats_label'):
            self.stats_label.configure(text=self._get_stats_text())
            
    def _create_item_card(self, item):
        """Cria card para um item. Pode ser sobrescrito para customização."""
        return ItemCard(self.list_container, item, self)
        
    def _load_items(self):
        """Carrega itens do serviço."""
        try:
            self.items = self.get_items(self.conexao)
        except Exception:
            logger.exception("Falha ao carregar %s", self.item_name_plural())
            CTkMessagebox(
                title="Erro",
                message=f"Erro ao carregar {self.item_name_plural()}.",
                icon="cancel"
            )
            self.items = []
            
    def _reload(self):
        """Recarrega itens e atualiza interface."""
        self._load_items()
        self._populate_list()
        
    # Métodos de ação (mantidos do código original)
    def _on_add(self):
        cls = self.modal_class_add()
        params = dict(conexao=self.conexao, service=self.service, master=self, callback=self._reload)
        if 'semestre' in inspect.signature(cls.__init__).parameters:
            params['semestre'] = self.semestre
        cls(**params)
        
    def _on_delete(self, item):
        try:
            self.delete_item(item)
            self._reload()
            CTkMessagebox(
                title="Sucesso",
                message=f"{self.item_name_singular().title()} excluído com sucesso!",
                icon="check"
            )
        except Exception:
            logger.exception("Erro ao deletar %s", self.get_id(item))
            CTkMessagebox(
                title="Erro",
                message=f"Não foi possível excluir {self.item_name_singular()}.",
                icon="cancel"
            )
            
    def _on_update(self, item):
        cls = self.modal_class_update()
        cls(conexao=self.conexao, service=self.service, master=self, callback=self._reload, item=item)
        
    def _on_select(self, item):
        key = self.get_id(item)
        if key in self.item_views and self.item_views[key].winfo_exists():
            win = self.item_views[key]
            try:
                win.deiconify()
                win.lift()
                win.focus_force()
            except Exception:
                logger.warning("Não conseguiu focar %s %s", self.item_name_singular(), key)
        else:
            try:
                win = self.detail_view_class()(item, self.conexao, self.service)
                win.protocol("WM_DELETE_WINDOW", lambda k=key: self._on_close(k))
                self.item_views[key] = win
            except Exception:
                logger.exception("Erro ao abrir detalhe de %s %s", self.item_name_singular(), key)
                CTkMessagebox(
                    title="Erro",
                    message=f"Não foi possível abrir {self.item_name_singular()}.",
                    icon="cancel"
                )
                
    def _on_close(self, key):
        win = self.item_views.pop(key, None)
        if win:
            win.destroy()
            
    # Métodos abstratos (mantidos do código original)
    @abstractmethod
    def get_items(self, conexao): ...
    
    @abstractmethod
    def modal_class_add(self): ...
    
    @abstractmethod
    def modal_class_update(self): ...
    
    @abstractmethod
    def detail_view_class(self): ...
    
    @abstractmethod
    def get_id(self, item): ...
    
    @abstractmethod
    def item_name(self, item): ...
    
    @abstractmethod
    def item_name_singular(self): ...
    
    @abstractmethod
    def item_name_plural(self): ...
    
    @abstractmethod
    def title_text(self): ...
    
    @abstractmethod
    def subtitle_text(self): ...
    
    @abstractmethod
    def add_button_text(self): ...
    
    @abstractmethod
    def delete_item(self, item): ...
    
    @abstractmethod
    def update_item(self, item): ...