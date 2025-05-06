import tkinter
import customtkinter

from app.components.sidebar import SidebarFrame
from app.components.semestres_list import SemestresFrame
from app.services.semestre_services import SemestreService

class PaginaInicial(customtkinter.CTk):
    def __init__(self, conexao):
        super().__init__()
        self.conexao = conexao
        self._configurar_janela()
        self._inicializar_estado()
        self._criar_interface()

    def _configurar_janela(self):
        self.title("Sistema de Gerenciamento Acadêmico")
        self.geometry("1000x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

    def _inicializar_estado(self):
        self.selected_appearance = tkinter.StringVar(value="Sistema")
        self.selected_theme = tkinter.StringVar(value="Azul")
        self.selected_scaling = tkinter.StringVar(value="100%")

    def _criar_interface(self):
        self.sidebar_frame = SidebarFrame(self, controller=self)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        self.semestres_frame = SemestresFrame(self.conexao, master=self)
        self.semestres_frame.grid(row=0, column=1, sticky="nsew")

    # Eventos
    def change_appearance_mode_event(self, new_mode: str):
        modo = {"Claro": "Light", "Escuro": "Dark", "Sistema": "System"}
        customtkinter.set_appearance_mode(modo.get(new_mode, "System"))
        self.selected_appearance.set(new_mode)

    def change_theme_mode_event(self, new_theme: str):
        temas = {
            "Azul": "blue",
            "Verde": "green",
            "Azul Escuro": "dark-blue",
            "Rosa": "app/themes/rose.json",
            "Violeta": "app/themes/violet.json",
            "Vaporwave": "app/themes/vaporwave.json",
        }
        customtkinter.set_default_color_theme(temas.get(new_theme, "blue"))
        self.selected_theme.set(new_theme)

        self._reconstruir_interface()

    def change_scaling_event(self, new_scaling: str):
        escala = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(escala)
        self.selected_scaling.set(new_scaling)

    def _reconstruir_interface(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._criar_interface()