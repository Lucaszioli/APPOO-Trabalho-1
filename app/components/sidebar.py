import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.configure(width=140, corner_radius=0)
        
        # Criar frama
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_rowconfigure(11, weight=1)

        # Widgets
        self.logo_label = customtkinter.CTkLabel(self.frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.frame, text="Botão 1")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.frame, text="Botão 2")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.frame, text="Botão 3")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.build_options()

    def build_options(self):
        # Aparência
        self.appearance_mode_label = customtkinter.CTkLabel(self.frame, text="Aparência:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.frame,
            values=["Claro", "Escuro", "Sistema"],
            command=self.controller.change_appearance_mode_event,
            variable=self.controller.selected_appearance
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Tema
        self.theme_mode_label = customtkinter.CTkLabel(self.frame, text="Tema:", anchor="w")
        self.theme_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.theme_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.frame,
            values=["Azul", "Verde", "Azul Escuro", "Rosa", "Violeta", "Vaporwave"],
            command=self.controller.change_theme_mode_event,
            variable=self.controller.selected_theme
        )
        self.theme_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        # Escala
        self.scaling_label = customtkinter.CTkLabel(self.frame, text="Escala:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.controller.change_scaling_event,
            variable=self.controller.selected_scaling
        )
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
