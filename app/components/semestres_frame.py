import logging
import tkinter
import customtkinter
from typing import Any, Dict, List, Optional
from CTkMessagebox import CTkMessagebox
from app.services.semestre_services import SemestreService
from app.components.modal_novo_semestre import ModalNovoSemestre

logger = logging.getLogger(__name__)

class SemestresFrame(customtkinter.CTkFrame):
    """Frame que exibe semestres cadastrados e permite adicionar/selecionar semestres."""
    def __init__(
        self,
        conexao: Any,
        master: Optional[tkinter.Widget] = None
    ) -> None:
        super().__init__(master)
        if conexao is None:
            raise ValueError("Conexão com o banco de dados não pode ser nula.")
        self.conexao = conexao
        self.semestres: List[Any] = []
        self.semestre_views: Dict[int, customtkinter.CTk] = {}
        self._configure_layout()
        self._load_semestres()
        self._create_widgets()

    def _configure_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def _load_semestres(self) -> None:
        try:
            self.semestres = SemestreService.listar_semestres(self.conexao)
        except Exception:
            logger.exception("Falha ao carregar semestres")
            self.semestres = []
            CTkMessagebox(title="Erro", message="Erro ao carregar semestres.", icon="cancel")

    def _create_widgets(self) -> None:
        self._create_title()
        self._create_add_button()
        self._create_list_frame()

    def _create_title(self) -> None:
        title = customtkinter.CTkLabel(
            self,
            text="Seja Bem-Vindo(a)",
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="nsew")
        subtitle = customtkinter.CTkLabel(
            self,
            text="Selecione um semestre:",
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        subtitle.grid(row=1, column=1, padx=20, pady=(0, 30), sticky="nsew")

    def _create_add_button(self) -> None:
        add_btn = customtkinter.CTkButton(
            self,
            text="Adicionar Semestre",
            command=self._on_add_semestre
        )
        add_btn.grid(row=4, column=1, padx=20, pady=(0, 10), sticky="nsew")

    def _create_list_frame(self) -> None:
        self.list_container = customtkinter.CTkScrollableFrame(
            self,
            width=300,
            height=400
        )
        self.list_container.grid(row=5, column=1, padx=20, pady=(0, 10), sticky="nsew")
        self.list_container.grid_rowconfigure(0, weight=1)
        self.list_container.grid_columnconfigure(0, weight=1)
        self._populate_list()

    def _populate_list(self) -> None:
        for widget in self.list_container.winfo_children():
            widget.destroy()
        if not self.semestres:
            label = customtkinter.CTkLabel(
                self.list_container,
                text="Nenhum semestre cadastrado.",
                font=customtkinter.CTkFont(size=14, slant="italic")
            )
            label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            return
        for idx, semestre in enumerate(self.semestres):
            if not hasattr(semestre, "id") or not hasattr(semestre, "nome"):
                continue
            btn = customtkinter.CTkButton(
                self.list_container,
                text=semestre.nome,
                command=lambda s=semestre: self._on_select_semestre(s)
            )
            btn.grid(row=idx, column=0, padx=20, pady=10, sticky="nsew")

    def _on_add_semestre(self) -> None:
        ModalNovoSemestre(
            conexao=self.conexao,
            master=self,
            callback=self._reload
        )

    def _on_select_semestre(self, semestre: Any) -> None:
        key = getattr(semestre, "id", None)
        if key is None:
            CTkMessagebox(
                title="Erro",
                message="Semestre inválido.",
                icon="cancel"
            )
            return
        window = self.semestre_views.get(key)
        if window and window.winfo_exists():
            try:
                window.deiconify()
                window.lift()
                window.focus_force()
            except Exception:
                logger.warning("Não foi possível focar a janela do semestre %s", semestre.nome)
            return
        try:
            from app.views.pagina_semestre import PaginaSemestre
            window = PaginaSemestre(semestre, self.conexao)
            window.protocol("WM_DELETE_WINDOW", lambda k=key: self._on_close_semestre(k))
            self.semestre_views[key] = window
        except Exception:
            logger.exception("Erro ao abrir janela do semestre %s", semestre.nome)
            CTkMessagebox(
                title="Erro",
                message="Não foi possível abrir a janela do semestre.",
                icon="cancel"
            )

    def _on_close_semestre(self, key: int) -> None:
        window = self.semestre_views.pop(key, None)
        if window:
            window.destroy()

    def _reload(self) -> None:
        self._load_semestres()
        self._populate_list()