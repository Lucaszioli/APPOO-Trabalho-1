import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller

        if not all(hasattr(controller, attr) for attr in [
            "change_appearance_mode_event",
            "change_theme_mode_event",
            "change_scaling_event",
            "selected_appearance",
            "selected_theme",
            "selected_scaling"
        ]):
            raise AttributeError("Controller não possui os atributos ou métodos esperados.")

        self.configure(width=140, corner_radius=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        try:
            self._criar_widgets()
        except Exception as e:
            print(f"Erro ao construir barra lateral: {e}")

    def _criar_widgets(self):
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.frame, text="Botão 1")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.frame, text="Botão 2")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.frame, text="Botão 3")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self._criar_opcoes()

    def _criar_opcoes(self):
        # Aparência
        customtkinter.CTkLabel(self.frame, text="Aparência:", anchor="w").grid(
            row=5, column=0, padx=20, pady=(10, 0)
        )

        customtkinter.CTkOptionMenu(
            self.frame,
            values=["Claro", "Escuro", "Sistema"],
            command=self.controller.change_appearance_mode_event,
            variable=self.controller.selected_appearance
        ).grid(row=6, column=0, padx=20, pady=(10, 10))

        # Tema
        customtkinter.CTkLabel(self.frame, text="Tema:", anchor="w").grid(
            row=7, column=0, padx=20, pady=(10, 0)
        )

        customtkinter.CTkOptionMenu(
            self.frame,
            values=["Azul", "Verde", "Azul Escuro", "Rosa", "Violeta", "Vaporwave"],
            command=self.controller.change_theme_mode_event,
            variable=self.controller.selected_theme
        ).grid(row=8, column=0, padx=20, pady=(10, 10))

        # Escala
        customtkinter.CTkLabel(self.frame, text="Escala:", anchor="w").grid(
            row=9, column=0, padx=20, pady=(10, 0)
        )

        customtkinter.CTkOptionMenu(
            self.frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.controller.change_scaling_event,
            variable=self.controller.selected_scaling
        ).grid(row=10, column=0, padx=20, pady=(10, 20))