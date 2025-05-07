import customtkinter
from app.services.semestre_services import SemestreService
from app.components.modal_nsemestre import ModalNovoSemestre
from CTkMessagebox import CTkMessagebox

class SemestresFrame(customtkinter.CTkFrame):
    def __init__(self, conexao, master=None):
        super().__init__(master)

        if conexao is None:
            raise ValueError("Conexão com o banco de dados não pode ser nula.")

        self.conexao = conexao
        self.semestres = []
        self.semestre_views = {}

        self._configurar_layout()
        self._carregar_semestres()
        self._criar_widgets()

    def _configurar_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def _carregar_semestres(self):
        try:
            self.semestres = SemestreService.listar_semestres(self.conexao)
        except Exception as e:
            self.semestres = []
            CTkMessagebox(title="Erro", message="Erro ao carregar semestres do banco de dados.", icon="cancel")
            print(f"[ERRO] Falha ao carregar semestres: {e}")

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

        self._popular_semestres()

    def _popular_semestres(self):
        if not self.semestres:
            aviso = customtkinter.CTkLabel(
                self.semestres_frame, text="Nenhum semestre cadastrado.",
                font=customtkinter.CTkFont(size=14, slant="italic")
            )
            aviso.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            return

        for i, semestre in enumerate(self.semestres):
            if not hasattr(semestre, "nome"):
                continue  # Pula semestres malformados

            btn = customtkinter.CTkButton(
                self.semestres_frame,
                text=semestre.nome,
                command=lambda s=semestre: self._selecionar_semestre(s)
            )
            btn.grid(row=i + 2, column=0, padx=20, pady=10, sticky="nsew")

    # Ações
    def _adicionar_semestre(self):
        ModalNovoSemestre(
            self.conexao,
            master=self,
            callback_atualizacao=self._recarregar_lista
        )

    def _selecionar_semestre(self, semestre):
        if not hasattr(semestre, "id") or not hasattr(semestre, "nome"):
            CTkMessagebox(
                title="Erro",
                message="Erro ao selecionar semestre. Semestre inválido.",
                icon="cancel"
            )
            print(f"[ERRO] Semestre inválido: {semestre}")
            return

        key = semestre.id
        window = self.semestre_views.get(key)

        if window is None or not window.winfo_exists():
            try:
                from app.windows.pagina_semestre import PaginaSemestre
                window = PaginaSemestre(semestre, self.conexao)
                window.protocol(
                    "WM_DELETE_WINDOW",
                    lambda k=key, w=window: self._fechar_semestre(k, w)
                )
                self.semestre_views[key] = window
            except Exception as e:
                CTkMessagebox(
                    title="Erro",
                    message="Não foi possível abrir a janela do semestre.",
                    icon="cancel"
                )
                print(f"[ERRO] Falha ao criar janela do semestre {semestre.nome}: {e}")
            return

        try:
            if window.state() == 'iconic':
                window.deiconify()
            window.lift()
            window.focus_force()
        except Exception as e:
            CTkMessagebox(
                title="Atenção",
                message="Não foi possível focar a janela do semestre.",
                icon="warning"
            )
            print(f"[AVISO] Falha ao focar janela do semestre {semestre.nome}: {e}")

            
    def _fechar_semestre(self, key, window):
        try:
            window.destroy()
        finally:
            self.semestre_views.pop(key, None)

    def _recarregar_lista(self):
        try:
            for widget in self.semestres_frame.winfo_children():
                widget.destroy()
            self._carregar_semestres()
            self._popular_semestres()
        except Exception as e:
            CTkMessagebox(title="Erro", message="Erro ao atualizar lista de semestres.", icon="cancel")
            print(f"[ERRO] Falha ao recarregar lista: {e}")
