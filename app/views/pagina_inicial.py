import customtkinter

# Configurações globais
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("app/themes/vaporwave.json")

TITULO_APP = "Hub Acadêmico"

class PaginaInicial(customtkinter.CTk):
    """Classe principal da interface inicial do Hub Acadêmico."""

    def __init__(self):
        super().__init__()
        self._configurar_janela()
        self._criar_sidebar()
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
        
    def _criar_sidebar(self):
        """Cria a barra lateral da interface."""
        self.sidebar = customtkinter.CTkFrame(master=self.frame, width=200)
        self.sidebar.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.sidebar.grid_rowconfigure(0, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        # Adiciona os botões na barra lateral
        self.botao_semestres = customtkinter.CTkButton(
            master=self.sidebar,
            text="Semestres",
            # command=self._abrir_semestres
        )
        self.botao_semestres.grid(row=0, column=0, padx=10, pady=10)
        self.botao_disciplinas = customtkinter.CTkButton(
            master=self.sidebar,
            text="Disciplinas",
            # command=self._abrir_disciplinas
        )
        self.botao_disciplinas.grid(row=1, column=0, padx=10, pady=10)
        self.botao_horarios = customtkinter.CTkButton(
            master=self.sidebar,
            text="Horários",
            # command=self._abrir_horarios
        )
        self.botao_horarios.grid(row=2, column=0, padx=10, pady=10)
        self.botao_notas = customtkinter.CTkButton(
            master=self.sidebar,
            text="Notas",
            # command=self._abrir_notas
        )
        self.botao_notas.grid(row=3, column=0, padx=10, pady=10)
        self.botao_configuracoes = customtkinter.CTkButton(
            master=self.sidebar,
            text="Configurações",
            # command=self._abrir_configuracoes
        )
        self.botao_configuracoes.grid(row=4, column=0, padx=10, pady=10)
        self.botao_sair = customtkinter.CTkButton(
            master=self.sidebar,
            text="Sair",
            # command=self._sair
        )
        self.botao_sair.grid(row=5, column=0, padx=10, pady=10)
