import tkinter
import customtkinter
import logging
from CTkMessagebox import CTkMessagebox
from app.ui.components.sidebar_toggle import SidebarToggle
from typing import Optional, Any

logger = logging.getLogger(__name__)

class BaseWindow(customtkinter.CTk):
    """
    Janela base com configuração moderna de layout e temas.
    """
    APPEARANCE_MAP = {"Claro": "Light", "Escuro": "Dark", "Sistema": "System"}
    COLOR_THEMES = {
        "Azul": "blue",
        "Verde": "green",
        "Azul Escuro": "dark-blue",
        "Rosa": "app/ui/themes/rose.json",
        "Violeta": "app/ui/themes/violet.json",
        "Vaporwave": "app/ui/themes/vaporwave.json",
    }
    SCALING_RANGE = (0.5, 2.0)
    DEFAULT_SIZE = (1200, 700)

    def __init__(self, title: str, service: Any) -> None:
        super().__init__()
        self.service = service
        self.selected_appearance = tkinter.StringVar(value="Sistema")
        self.selected_theme = tkinter.StringVar(value="Azul")
        self.selected_scaling = tkinter.StringVar(value="100%")
        self._configure_window(title)
        self._setup_initial_theme()
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
        width, height = self.DEFAULT_SIZE
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.minsize(800, 500)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_initial_theme(self) -> None:
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("blue")

    def _create_sidebar(self) -> None:
        self.sidebar = SidebarToggle(self, controller=self)
        self.sidebar.configure(corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")

    def _create_body(self) -> None:
        raise NotImplementedError("Subclasses devem implementar _create_body()")

    def change_appearance_mode_event(self, new_mode: str) -> None:
        modo = self.APPEARANCE_MAP.get(new_mode)
        if not modo:
            logger.warning("Modo de aparência desconhecido: %s", new_mode)
            return
        try:
            customtkinter.set_appearance_mode(modo)
            self.selected_appearance.set(new_mode)
            logger.info("Modo de aparência alterado para: %s", new_mode)
        except Exception:
            logger.exception("Erro ao alterar modo de aparência")
            CTkMessagebox(
                title="Erro",
                message=f"Não foi possível alterar para o modo '{new_mode}'.",
                icon="cancel"
            )

    def change_theme_mode_event(self, new_theme: str) -> None:
        caminho = self.COLOR_THEMES.get(new_theme)
        if not caminho:
            logger.warning("Tema não reconhecido: %s", new_theme)
            return
        try:
            customtkinter.set_default_color_theme(caminho)
            self.selected_theme.set(new_theme)
            self._rebuild_ui()
            logger.info("Tema alterado para: %s", new_theme)
        except Exception:
            logger.exception("Erro ao aplicar tema '%s'", new_theme)
            CTkMessagebox(
                title="Erro",
                message=f"Não foi possível aplicar o tema '{new_theme}'.",
                icon="cancel"
            )

    def change_scaling_event(self, new_scaling: str) -> None:
        try:
            scale = int(new_scaling.rstrip("%")) / 100
            min_s, max_s = self.SCALING_RANGE
            if not (min_s <= scale <= max_s):
                raise ValueError("Escala fora do intervalo permitido.")
            customtkinter.set_widget_scaling(scale)
            self.selected_scaling.set(new_scaling)
            logger.info("Escala alterada para: %s", new_scaling)
        except ValueError as e:
            logger.error("Escala inválida: %s - %s", new_scaling, str(e))
            CTkMessagebox(
                title="Erro de Escala",
                message="Valor de escala inválido. Use entre 80% e 120%.",
                icon="cancel"
            )
        except Exception:
            logger.exception("Erro inesperado ao alterar escala")
            CTkMessagebox(
                title="Erro",
                message="Não foi possível alterar a escala da interface.",
                icon="cancel"
            )

    def _rebuild_ui(self) -> None:
        try:
            # Corrigido: verificação mais robusta da sidebar
            sidebar_open = (
                hasattr(self, 'sidebar') and 
                self.sidebar and
                hasattr(self.sidebar, 'sidebar') and 
                self.sidebar.sidebar and 
                self.sidebar.sidebar.winfo_exists()
            )
            
            for widget in self.winfo_children():
                widget.destroy()
                
            self._create_sidebar()
            self._create_body()
            
            if sidebar_open and hasattr(self.sidebar, '_open_sidebar'):
                self.sidebar._open_sidebar()
        except Exception:
            logger.exception("Erro ao reconstruir interface")
            CTkMessagebox(
                title="Erro",
                message="Erro ao aplicar novo tema. Reinicie a aplicação.",
                icon="cancel"
            )

    def _on_closing(self) -> None:
        try:
            # Corrigido: verificação mais robusta antes de fechar sidebar
            if (hasattr(self, 'sidebar') and 
                self.sidebar and
                hasattr(self.sidebar, 'sidebar') and 
                self.sidebar.sidebar and
                hasattr(self.sidebar, '_close_sidebar')):
                self.sidebar._close_sidebar()
            self.destroy()
        except Exception:
            logger.exception("Erro ao fechar janela")
            self.destroy()

    def show_info_message(self, title: str, message: str) -> None:
        CTkMessagebox(title=title, message=message, icon="info")

    def show_error_message(self, title: str, message: str) -> None:
        CTkMessagebox(title=title, message=message, icon="cancel")

    def show_success_message(self, title: str, message: str) -> None:
        CTkMessagebox(title=title, message=message, icon="check")
