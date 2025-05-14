from abc import ABC, abstractmethod
import logging
import customtkinter
from CTkMessagebox import CTkMessagebox

logger = logging.getLogger(__name__)

class BaseListFrame(customtkinter.CTkFrame, ABC):
    """Frame genérico para listar entidades e abrir modais ou janelas de detalhe."""
    def __init__(self, conexao, semestre_service, semestre, master=None):
        super().__init__(master)
        if conexao is None:
            raise ValueError("Conexão não pode ser nula.")
        self.conexao = conexao
        self.semestre = semestre
        self.semestre_service = semestre_service
        self.items = []
        self.item_views = {}
        self._configure_layout()
        self._load_items()
        self._create_widgets()

    def _configure_layout(self):
        # configuração de grid comum
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def _load_items(self):
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

    def _create_widgets(self):
        # título
        label_title = customtkinter.CTkLabel(
            self,
            text=self.title_text(),
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        label_title.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="nsew")
        label_sub = customtkinter.CTkLabel(
            self,
            text=self.subtitle_text(),
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        label_sub.grid(row=1, column=1, padx=20, pady=(0, 30), sticky="nsew")

        # botão de adicionar
        btn_add = customtkinter.CTkButton(
            self,
            text=self.add_button_text(),
            command=self._on_add
        )
        btn_add.grid(row=4, column=1, padx=20, pady=(0, 10), sticky="nsew")

        # lista scrollable
        self.list_container = customtkinter.CTkScrollableFrame(
            self,
            width=300,
            height=400
        )
        self.list_container.grid(row=5, column=1, padx=20, pady=(0, 10), sticky="nsew")
        self.list_container.grid_rowconfigure(0, weight=1)
        self.list_container.grid_columnconfigure(0, weight=1)
        self._populate_list()

    def _populate_list(self):
        for w in self.list_container.winfo_children():
            w.destroy()
        if not self.items:
            label = customtkinter.CTkLabel(
                self.list_container,
                text=f"Nenhum {self.item_name_plural()}.",
                font=customtkinter.CTkFont(size=14, slant="italic"),
            )
            label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            return
        for idx, item in enumerate(self.items):
            name = self.item_name(item)
            btn = customtkinter.CTkButton(
                self.list_container,
                text=name,
                command=lambda it=item: self._on_select(it)
            )
            btn.grid(row=idx, column=0, padx=(20,2), pady=10, sticky="nsew")
            delete_btn = customtkinter.CTkButton(
                self.list_container,
                text="X",
                command=lambda it=item: self._on_delete(it),
                fg_color="red",
                width=30,
            )
            delete_btn.grid(row=idx, column=1, padx=(0,2), pady=10, sticky="nsew")
            uptate_btn = customtkinter.CTkButton(
                self.list_container,
                text="⚙️",
                command=lambda it=item: self._on_update(it),
                fg_color="blue",
                width=30,
            )
            uptate_btn.grid(row=idx, column=2, pady=10, sticky="nsew")

    def _on_add(self):
        # abre modal de adicionar
        cls = self.modal_class_add()
        cls(conexao=self.conexao, semestre_service = self.semestre_service, master=self, callback=self._reload)
        
    def _on_delete(self, item):
        # deleta item
        try:
            self.delete_item(item)
            self._reload()
            print(f"{self.item_name_singular()} deletado com sucesso.")
        except Exception:
            logger.exception("Erro ao deletar %s %s", self.item_name_singular(), self.get_id(item))
            CTkMessagebox(
                title="Erro",
                message=f"Não foi possível deletar {self.item_name_singular()}.",
                icon="cancel"
            )
            
    def _on_update(self, item):
        # abre modal de atualizar
        cls = self.modal_class_update()
        cls(conexao=self.conexao, semestre_service=self.semestre_service, master=self, callback=self._reload, item=item)

    def _on_select(self, item):
        key = self.get_id(item)
        if key in self.item_views and self.item_views[key].winfo_exists():
            win = self.item_views[key]
            try:
                win.deiconify(); win.lift(); win.focus_force()
            except Exception:
                logger.warning("Não conseguiu focar %s %s", self.item_name_singular(), key)
        else:
            try:
                win = self.detail_view_class()(item, self.conexao)
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

    def _reload(self):
        self._load_items()
        self._populate_list()

    # Métodos abstratos que a subclasse deve implementar:
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
