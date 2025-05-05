import tkinter
import tkinter.messagebox as messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class PaginaInicial(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Sistema de Gerenciamento Acadêmico")
        self.geometry("1000x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Barra lateral
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Sidebar buttons
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Botão 1")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Botão 2")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Botão 3")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        
        # Sidebar configs
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Aparência:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Claro", "Escuro", "Sistema"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.theme_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.theme_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.theme_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Azul", "Verde", "Azul Escuro", "Rosa"],
                                                                   command=self.change_theme_mode_event)
        self.theme_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Escala:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
        
    # Funções
    def change_appearance_mode_event(self, new_appearance_mode: str):
        if new_appearance_mode == "Claro":
            new_appearance_mode = "Light"
        elif new_appearance_mode == "Escuro":
            new_appearance_mode = "Dark"
        elif new_appearance_mode == "Sistema":
            new_appearance_mode = "System"
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def change_theme_mode_event(self, new_theme: str):
        if new_theme == "Azul":
            new_theme = "blue"
        elif new_theme == "Verde":
            new_theme = "green"
        elif new_theme == "Azul Escuro":
            new_theme = "dark-blue"
        elif new_theme == "Rosa":
            new_theme = "app/themes/rose.json"
        customtkinter.set_default_color_theme(new_theme)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
        
        
    
        