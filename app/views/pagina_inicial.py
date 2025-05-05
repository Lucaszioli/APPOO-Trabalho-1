import tkinter
import customtkinter

from app.components.sidebar import SidebarFrame

class PaginaInicial(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Janela
        self.title("Sistema de Gerenciamento Acadêmico")
        self.geometry("1000x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Controle de estado
        self.selected_appearance = tkinter.StringVar(value="Sistema")
        self.selected_theme = tkinter.StringVar(value="Azul")
        self.selected_scaling = tkinter.StringVar(value="100%")

        self.build_ui()

    def build_ui(self):
        self.sidebar_frame = SidebarFrame(self, controller=self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

    # Eventos
    def change_appearance_mode_event(self, new_mode: str):
        mode_map = {"Claro": "Light", "Escuro": "Dark", "Sistema": "System"}
        customtkinter.set_appearance_mode(mode_map.get(new_mode, "System"))
        self.selected_appearance.set(new_mode)

    def change_theme_mode_event(self, new_theme: str):
        theme_map = {
            "Azul": "blue",
            "Verde": "green",
            "Azul Escuro": "dark-blue",
            "Rosa": "app/themes/rose.json",
            "Violeta": "app/themes/violet.json"
        }
        customtkinter.set_default_color_theme(theme_map.get(new_theme, "blue"))
        self.selected_theme.set(new_theme)

        # Recriar UI
        for widget in self.winfo_children():
            widget.destroy()
        self.build_ui()

    def change_scaling_event(self, new_scaling: str):
        scale = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(scale)
        self.selected_scaling.set(new_scaling)
