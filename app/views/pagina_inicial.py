import tkinter
import tkinter.messagebox as messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
customtkinter.set_default_color_theme("app/themes/vaporwave.json")  # Themes: "blue", "green", "dark-blue"

class PaginaInicial(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento Acadêmico")
        self.geometry("1000x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main
        main = customtkinter.CTkFrame(self)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        
        # Header
        header = customtkinter.CTkFrame(main)
        header.grid(row=0, column=0, sticky="nsew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_rowconfigure(0, weight=1)
        
        # Title
        title = customtkinter.CTkLabel(header, text="Sistema de Gerenciamento Acadêmico")
        title.grid(row=0, column=0, padx=20, pady=20)
        title.grid_columnconfigure(0, weight=1)
        title.grid_rowconfigure(0, weight=1)
        