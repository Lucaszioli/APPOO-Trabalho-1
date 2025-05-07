import tkinter
import tkinter.messagebox
import customtkinter
from CTkMessagebox import CTkMessagebox
from app.components.sidebar import SidebarToggle
from app.components.semestres_list import SemestresFrame

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
        self._inicializar_estado()
        self._criar_interface()

    def _configurar_janela(self):
        self.title("Semestre " + self.semestre.nome)
        self.geometry("1000x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
    def _inicializar_estado(self):
        self.selected_appearance = tkinter.StringVar(value="Sistema")
        self.selected_theme = tkinter.StringVar(value="Azul")
        self.selected_scaling = tkinter.StringVar(value="100%")
        
    def _criar_interface(self):
        try:
            self.sidebar = SidebarToggle(self, controller=self)
            self.sidebar.configure(corner_radius=0)
            self.sidebar.grid(row=0, column=0, sticky="ns")
            
            self.semestres_frame = SemestresFrame(self.conexao, master=self)
            self.semestres_frame.grid(row=0, column=1, sticky="nsew")

        except Exception as e:
            print(f"Erro ao criar interface: {e}")
            tkinter.messagebox.showerror(
                title="Erro",
                message="Erro ao inicializar a interface gráfica.",
                icon="cancel"
            )
    
    # Eventos
    def change_appearance_mode_event(self, new_mode: str):
        modo_map = {"Claro": "Light", "Escuro": "Dark", "Sistema": "System"}
        if new_mode not in modo_map:
            print(f"[Aviso] Modo de aparência desconhecido: {new_mode}")
            return
        customtkinter.set_appearance_mode(modo_map[new_mode])
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
        caminho_tema = temas.get(new_theme)
        if not caminho_tema:
            print(f"[Aviso] Tema não reconhecido: {new_theme}")
            return

        try:
            customtkinter.set_default_color_theme(caminho_tema)
            self.selected_theme.set(new_theme)
            self._reconstruir_interface()
        except Exception as e:
            print(f"Erro ao aplicar tema '{new_theme}': {e}")
            CTkMessagebox(
                title="Erro",
                message=f"Erro ao aplicar o tema '{new_theme}'.",
                icon="cancel"
            )

    def change_scaling_event(self, new_scaling: str):
        try:
            escala = int(new_scaling.replace("%", "")) / 100
            if not 0.5 <= escala <= 2:
                raise ValueError("Escala fora do intervalo permitido.")
            customtkinter.set_widget_scaling(escala)
            self.selected_scaling.set(new_scaling)
        except ValueError:
            print(f"[Erro] Escala inválida: {new_scaling}")
            CTkMessagebox(
                title="Erro",
                message="Valor de escala inválido. Use entre 50% e 200%.",
                icon="cancel"
            )

    def _reconstruir_interface(self):
        try:
            for widget in self.winfo_children():
                widget.destroy()
            self._criar_interface()
        except Exception as e:
            print(f"Erro ao reconstruir interface: {e}")
            CTkMessagebox(
                title="Erro",
                message="Erro ao reconstruir interface.",
                icon="cancel"
            )