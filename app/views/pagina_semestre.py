import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class PaginaSemestre(customtkinter.CTk):
    def __init__(self, nome_semestre):
        super().__init__()

        # configure window
        self.title("Semestre " + nome_semestre)
        self.geometry(f"{1100}x{580}")

       