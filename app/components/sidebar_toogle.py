import logging
import customtkinter
from CTkMessagebox import CTkMessagebox
from typing import Any

logger = logging.getLogger(__name__)

class SidebarToggle(customtkinter.CTkFrame):
    """Componente que gerencia a abertura e fechamento da sidebar de configurações."""
    APPEARANCE_OPTIONS = ["Claro", "Escuro", "Sistema"]
    THEME_OPTIONS = ["Azul", "Verde", "Azul Escuro", "Rosa", "Violeta", "Vaporwave"]
    SCALING_OPTIONS = ["80%", "90%", "100%", "110%", "120%"]

    def __init__(
        self,
        master: customtkinter.CTk,
        controller: Any,
        *args,
        **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.sidebar: customtkinter.CTkFrame = None

        self.open_button = customtkinter.CTkButton(
            self,
            text="≡",
            width=40,
            height=40,
            command=self._open_sidebar
        )
        self.open_button.grid(row=0, column=0, padx=10, pady=10)

    def _open_sidebar(self) -> None:
        if self.sidebar and self.sidebar.winfo_exists():
            return
        try:
            self.sidebar = customtkinter.CTkFrame(self.master, width=200, corner_radius=0)
            self.sidebar.grid(row=0, column=0, sticky="ns")
            self.sidebar.grid_columnconfigure(0, weight=1)
            self.sidebar.grid_rowconfigure(2, weight=1)

            customtkinter.CTkLabel(
                self.sidebar,
                text="Menu",
                font=customtkinter.CTkFont(size=20, weight="bold")
            ).grid(row=0, column=0, pady=(20, 10), sticky="ew")

            customtkinter.CTkButton(
                self.sidebar,
                text="X",
                width=30,
                height=30,
                command=self._close_sidebar
            ).grid(row=1, column=0, pady=10, sticky="ew")

            self._add_options()
        except Exception:
            logger.exception("Falha ao abrir sidebar")
            CTkMessagebox(title="Erro", message="Não foi possível abrir o menu.", icon="cancel")

    def _close_sidebar(self) -> None:
        if self.sidebar:
            self.sidebar.grid_forget()
            self.sidebar.destroy()
            self.sidebar = None

    def _add_options(self) -> None:
        # Aparência
        customtkinter.CTkLabel(
            self.sidebar,
            text="Aparência:",
            anchor="w"
        ).grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        customtkinter.CTkOptionMenu(
            self.sidebar,
            values=self.APPEARANCE_OPTIONS,
            variable=self.controller.selected_appearance,
            command=self.controller.change_appearance_mode_event
        ).grid(row=4, column=0, padx=20, pady=(5, 10), sticky="ew")

        # Tema
        customtkinter.CTkLabel(
            self.sidebar,
            text="Tema:",
            anchor="w"
        ).grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        customtkinter.CTkOptionMenu(
            self.sidebar,
            values=self.THEME_OPTIONS,
            variable=self.controller.selected_theme,
            command=self.controller.change_theme_mode_event
        ).grid(row=6, column=0, padx=20, pady=(5, 10), sticky="ew")

        # Escala
        customtkinter.CTkLabel(
            self.sidebar,
            text="Escala:",
            anchor="w"
        ).grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        customtkinter.CTkOptionMenu(
            self.sidebar,
            values=self.SCALING_OPTIONS,
            variable=self.controller.selected_scaling,
            command=self.controller.change_scaling_event
        ).grid(row=8, column=0, padx=20, pady=(5, 20), sticky="ew")