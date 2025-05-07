import tkinter
import customtkinter
import logging
from CTkMessagebox import CTkMessagebox
from app.components.sidebar import SidebarToggle

logger = logging.getLogger(__name__)

class BaseWindow(customtkinter.CTk):
    """
    Janela base com configuração padrão de tamanho, grade e opções de tema/aparência.
    """

    APPEARANCE_MAP = {"Claro": "Light", "Escuro": "Dark", "Sistema": "System"}
    COLOR_THEMES = {
        "Azul": "blue",
        "Verde": "green",
        "Azul Escuro": "dark-blue",
        "Rosa": "app/themes/rose.json",
        "Violeta": "app/themes/violet.json",
        "Vaporwave": "app/themes/vaporwave.json",
    }
    SCALING_RANGE = (0.5, 2.0)
    DEFAULT_SIZE = (1000, 600)

    def __init__(self, conexao, title: str):
        super().__init__()
        if conexao is None:
            raise ValueError("Conexão com o banco de dados não pode ser nula.")
        self.conexao = conexao

        # Estado de interface
        self.selected_appearance = tkinter.StringVar(value="Sistema")
        self.selected_theme      = tkinter.StringVar(value="Azul")
        self.selected_scaling    = tkinter.StringVar(value="100%")

        self._configure_window(title)
        self._create_sidebar()
        try:
            self._create_body()
        except Exception:
            logger.exception("Erro ao criar o corpo da janela")
            CTkMessagebox(
                title="Erro",
                message="Falha ao inicializar a interface gráfica.",
                icon="cancel"
            )

    def _configure_window(self, title: str) -> None:
        """Define título, tamanho e configuração de grid."""
        width, height = self.DEFAULT_SIZE
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

    def _create_sidebar(self) -> None:
        """Instancia o componente de sidebar com as opções de configuração."""
        self.sidebar = SidebarToggle(self, controller=self)
        self.sidebar.configure(corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")

    def _create_body(self) -> None:
        """
        Constrói a parte central da janela. Deve ser implementado pelas subclasses.
        """
        raise NotImplementedError

    def change_appearance_mode_event(self, new_mode: str) -> None:
        """Callback para alterar modo de aparência (claro/escuro/sistema)."""
        modo = self.APPEARANCE_MAP.get(new_mode)
        if not modo:
            logger.warning("Modo de aparência desconhecido: %s", new_mode)
            return
        customtkinter.set_appearance_mode(modo)
        self.selected_appearance.set(new_mode)

    def change_theme_mode_event(self, new_theme: str) -> None:
        """Callback para alterar tema de cores."""
        caminho = self.COLOR_THEMES.get(new_theme)
        if not caminho:
            logger.warning("Tema não reconhecido: %s", new_theme)
            return
        try:
            customtkinter.set_default_color_theme(caminho)
            self.selected_theme.set(new_theme)
            self._rebuild_ui()
        except Exception:
            logger.exception("Erro ao aplicar tema '%s'", new_theme)
            CTkMessagebox(
                title="Erro",
                message=f"Não foi possível aplicar o tema '{new_theme}'.",
                icon="cancel"
            )

    def change_scaling_event(self, new_scaling: str) -> None:
        """Callback para alterar escala de widgets (50%–200%)."""
        try:
            scale = int(new_scaling.rstrip("%")) / 100
            min_s, max_s = self.SCALING_RANGE
            if not (min_s <= scale <= max_s):
                raise ValueError("Escala fora do intervalo permitido.")
            customtkinter.set_widget_scaling(scale)
            self.selected_scaling.set(new_scaling)
        except Exception:
            logger.error("Escala inválida: %s", new_scaling)
            CTkMessagebox(
                title="Erro",
                message="Valor de escala inválido. Use entre 50% e 200%.",
                icon="cancel"
            )

    def _rebuild_ui(self) -> None:
        """Reconstrói toda a interface (útil após troca de tema/escala)."""
        for widget in self.winfo_children():
            widget.destroy()
        self._create_sidebar()
        self._create_body()
