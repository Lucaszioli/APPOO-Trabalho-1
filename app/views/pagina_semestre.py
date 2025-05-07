import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class PaginaSemestre(customtkinter.CTk):
    def __init__(self, nome_semestre, conexao):
        super().__init__()

        if conexao is None:
            raise ValueError("Conexão com o banco de dados não pode ser nula.")

        self.conexao = conexao
        self.nome_semestre = nome_semestre
        
        self._configurar_janela()

    def _configurar_janela(self):
        self.title("Semestre " + self.nome_semestre)
        self.geometry("1000x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

       