import tkinter
import tkinter.messagebox
import customtkinter
from app.models.semestre import Semestre

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")


class PaginaSemestre(customtkinter.CTk):
    def __init__(self, Semestre, conexao):
        super().__init__()

        if conexao is None:
            raise ValueError("Conexão com o banco de dados não pode ser nula.")

        self.conexao = conexao
        self.semestre = Semestre
        
        self._configurar_janela()

    def _configurar_janela(self):
        self.title("Semestre " + self.semestre.nome)
        self.geometry("1000x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

       