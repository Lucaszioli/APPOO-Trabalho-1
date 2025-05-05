import tkinter
import tkinter.messagebox as messagebox
import customtkinter


# Configurações iniciais globais do CustomTkinter
customtkinter.set_appearance_mode("System")  # "System", "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # "blue", "green", "dark-blue", ou caminho .json


class PaginaInicial(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Configurações da janela principal
        self.title("Sistema de Gerenciamento Acadêmico")
        self.geometry("1000x600")
        self.configure_grid()
        
        # Variáveis de estado
        self.selected_appearance = tkinter.StringVar(value="Sistema")
        self.selected_theme = tkinter.StringVar(value="Azul")
        self.selected_scaling = tkinter.StringVar(value="100%")
        
        # Criação da interface
        self.setup_ui()

    def configure_grid(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def setup_ui(self):
        self.setup_sidebar()

    def setup_sidebar(self):
        # Frame da barra lateral
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botões da barra lateral
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Botão 1")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Botão 2")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Botão 3")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Opções de aparência
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Aparência:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Claro", "Escuro", "Sistema"],
            command=self.change_appearance_mode_event,
            variable=self.selected_appearance
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Opções de tema
        self.theme_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.theme_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.theme_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Azul", "Verde", "Azul Escuro", "Rosa"],
            command=self.change_theme_mode_event,
            variable=self.selected_theme
        )
        self.theme_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        # Opções de escala
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Escala:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
            variable=self.selected_scaling
        )
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))

    # Métodos de eventos
    def change_appearance_mode_event(self, new_appearance_mode: str):
        self.selected_appearance.set(new_appearance_mode)
        mapping = {
            "Claro": "Light", 
            "Escuro": "Dark", 
            "Sistema": "System"
        }
        customtkinter.set_appearance_mode(mapping.get(new_appearance_mode, "System"))

    def change_theme_mode_event(self, new_theme: str):
        self.selected_theme.set(new_theme)
        theme_map = {
            "Azul": "blue",
            "Verde": "green",
            "Azul Escuro": "dark-blue",
            "Rosa": "app/themes/rose.json"
        }
        theme_path = theme_map.get(new_theme, "blue")
        customtkinter.set_default_color_theme(theme_path)

        for widget in self.winfo_children():
            widget.destroy()
        self.configure_grid()
        self.setup_ui()

    def change_scaling_event(self, new_scaling: str):
        self.selected_scaling.set(new_scaling)
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)