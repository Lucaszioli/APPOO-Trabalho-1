import customtkinter
from CTkMessagebox import CTkMessagebox

class SidebarToggle(customtkinter.CTkFrame):

    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.sidebar = None

        # Botão para abrir a sidebar
        self.open_button = customtkinter.CTkButton(
            self,
            text="≡",
            width=40,
            height=40,
            command=self._abrir_sidebar
        )
        self.open_button.grid(row=0, column=0, padx=10, pady=10)

    def _abrir_sidebar(self):
        # Evita múltiplas instâncias abertas
        if self.sidebar and hasattr(self.sidebar, 'winfo_exists') and self.sidebar.winfo_exists():
            return

        try:
            # Cria frame da sidebar
            self.sidebar = customtkinter.CTkFrame(
                self.master,
                width=200,
                corner_radius=0
            )
            self.sidebar.grid(row=0, column=0, sticky="ns")
            self.sidebar.grid_columnconfigure(0, weight=1)
            self.sidebar.grid_rowconfigure(2, weight=1)

            # Título centralizado
            logo = customtkinter.CTkLabel(
                self.sidebar,
                text="Menu",
                font=customtkinter.CTkFont(size=20, weight="bold")
            )
            logo.grid(row=0, column=0, pady=(20, 10), sticky="ew")

            # Botão fechar centralizado
            close_btn = customtkinter.CTkButton(
                self.sidebar,
                text="X",
                width=30,
                height=30,
                command=self._fechar_sidebar
            )
            close_btn.grid(row=1, column=0, pady=10, sticky="ew")

            # Opções de configuração
            self._criar_opcoes()

        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Não foi possível abrir o menu: {e}",
                icon="cancel"
            )

    def _fechar_sidebar(self):
        if self.sidebar:
            try:
                self.sidebar.grid_forget()
                self.sidebar.destroy()
            finally:
                self.sidebar = None

    def _criar_opcoes(self):
        # Aparência
        customtkinter.CTkLabel(
            self.sidebar,
            text="Aparência:",
            anchor="w"
        ).grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        customtkinter.CTkOptionMenu(
            self.sidebar,
            values=["Claro", "Escuro", "Sistema"],
            command=self.controller.change_appearance_mode_event,
            variable=self.controller.selected_appearance
        ).grid(row=4, column=0, padx=20, pady=(5, 10), sticky="ew")

        # Tema
        customtkinter.CTkLabel(
            self.sidebar,
            text="Tema:",
            anchor="w"
        ).grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")

        customtkinter.CTkOptionMenu(
            self.sidebar,
            values=["Azul", "Verde", "Azul Escuro", "Rosa", "Violeta", "Vaporwave"],
            command=self.controller.change_theme_mode_event,
            variable=self.controller.selected_theme
        ).grid(row=6, column=0, padx=20, pady=(5, 10), sticky="ew")

        # Escala
        customtkinter.CTkLabel(
            self.sidebar,
            text="Escala:",
            anchor="w"
        ).grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")

        customtkinter.CTkOptionMenu(
            self.sidebar,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.controller.change_scaling_event,
            variable=self.controller.selected_scaling
        ).grid(row=8, column=0, padx=20, pady=(5, 20), sticky="ew")
