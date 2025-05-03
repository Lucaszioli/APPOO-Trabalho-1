import customtkinter
from .lista_semestres import Semestres_Card

# Configurações globais
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("app/themes/vaporwave.json")

TITULO_APP = "Hub Acadêmico"

class PaginaInicial(customtkinter.CTk):
    """Classe principal da interface inicial do Hub Acadêmico."""

    def __init__(self):
        super().__init__()
        self._configurar_janela()
        self._criar_titulo()
        # self._criar_card_semestres()

    def _configurar_janela(self):
        """Define propriedades da janela principal."""
        self.title(TITULO_APP)
        largura = self.winfo_screenwidth()
        altura = self.winfo_screenheight()
        self.geometry(f"{largura}x{altura}")
        
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(fill="both", expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def _criar_titulo(self):
        """Cria e posiciona os widgets da interface."""
        self.titulo = customtkinter.CTkLabel(
            master=self.frame,
            text= "Seja bem-vindo ao " + TITULO_APP,
            font=customtkinter.CTkFont(size=28, weight="bold"),
            anchor="center"
        )
        self.titulo.grid(row=0, column=0, padx=20, pady=20, sticky="n")