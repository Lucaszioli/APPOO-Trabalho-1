import customtkinter
from app.services.semestre_services import SemestreService

class SemestresFrame(customtkinter.CTkFrame):
    def __init__(self, conexao, master=None):
        super().__init__(master)
        self.conexao = conexao
        self.semestres = []
        self._configurar_layout()
        self._carregar_semestres()
        self._criar_widgets()

    def _configurar_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def _carregar_semestres(self):
        self.semestres = SemestreService.listar_semestres(self.conexao)

    def _criar_widgets(self):
        self._criar_titulo()
        self._criar_botao_adicionar()
        self._criar_lista_semestres()

    def _criar_titulo(self):
        titulo = customtkinter.CTkLabel(
            self, text="Seja Bem-Vindo(a)", font=customtkinter.CTkFont(size=24, weight="bold")
        )
        titulo.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="nsew")

        subtitulo = customtkinter.CTkLabel(
            self, text="Selecione um semestre:", font=customtkinter.CTkFont(size=15, weight="bold")
        )
        subtitulo.grid(row=1, column=1, padx=20, pady=(0, 30), sticky="nsew")

    def _criar_botao_adicionar(self):
        btn_adicionar = customtkinter.CTkButton(
            self, text="Adicionar Semestre", command=self._adicionar_semestre
        )
        btn_adicionar.grid(row=4, column=1, padx=20, pady=(0, 10), sticky="nsew")

    def _criar_lista_semestres(self):
        self.semestres_frame = customtkinter.CTkScrollableFrame(self, width=300, height=400)
        self.semestres_frame.grid(row=5, column=1, padx=20, pady=(0, 10), sticky="nsew")
        self.semestres_frame.grid_rowconfigure(0, weight=1)
        self.semestres_frame.grid_columnconfigure(0, weight=1)

        for i, semestre in enumerate(self.semestres):
            btn = customtkinter.CTkButton(
                self.semestres_frame,
                text=semestre.nome,
                command=lambda s=semestre: self._selecionar_semestre(s)
            )
            btn.grid(row=i+2, column=0, padx=20, pady=10, sticky="nsew")

    # Ações
    def _adicionar_semestre(self):
        ModalNovoSemestre(self.conexao, master=self, callback_atualizacao=self._recarregar_lista)
             
    def _selecionar_semestre(self, semestre):
        print(f"Selecionado: {semestre.nome}")
        
    def _recarregar_lista(self):
        # Remove widgets antigos
        for widget in self.semestres_frame.winfo_children():
            widget.destroy()

        # Recarrega do banco
        self._carregar_semestres()

        # Recria os botões
        for i, semestre in enumerate(self.semestres):
            btn = customtkinter.CTkButton(
                self.semestres_frame,
                text=semestre.nome,
                command=lambda s=semestre: self._selecionar_semestre(s)
            )
            btn.grid(row=i + 2, column=0, padx=20, pady=10, sticky="nsew")

        
class ModalNovoSemestre(customtkinter.CTkToplevel):
    def __init__(self, conexao, master=None, callback_atualizacao=None):
        super().__init__(master)
        self.conexao = conexao
        self.callback_atualizacao = callback_atualizacao
        self.title("Adicionar Novo Semestre")
        self.geometry("400x300")
        self._criar_widgets()

    def _criar_widgets(self):
        label_nome = customtkinter.CTkLabel(self, text="Nome do Semestre:")
        label_nome.pack(pady=10)

        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.pack(pady=10)

        btn_adicionar = customtkinter.CTkButton(self, text="Adicionar", command=self._adicionar_semestre)
        btn_adicionar.pack(pady=20)

    def _adicionar_semestre(self):
        nome = self.entry_nome.get()
        if nome:
            SemestreService.criar(nome, "2023-01-01", "2023-12-31", self.conexao)
            if self.callback_atualizacao:
                self.callback_atualizacao()
            self.destroy()

        