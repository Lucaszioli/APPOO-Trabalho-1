import customtkinter
from CTkMessagebox import CTkMessagebox
from app.components.date_picker import CTkDatePicker
from datetime import datetime
from app.services.semestre_services import SemestreService
from app.errors.nomeSemestre import NomeRepetidoError
class ModalNovoSemestre(customtkinter.CTkToplevel):
    def __init__(self, conexao, master=None, callback_atualizacao=None):
        super().__init__(master)
        
        if conexao is None:
            CTkMessagebox(title="Erro", message="Erro: conexão com banco de dados não foi fornecida.", icon="cancel")
            self.destroy()
            return
        
        self.conexao = conexao
        self.callback_atualizacao = callback_atualizacao
        self.title("Adicionar Novo Semestre")
        self.geometry("400x300")
        self._criar_widgets()

    def _criar_widgets(self):
        customtkinter.CTkLabel(self, text="Nome do Semestre:").pack()
        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.pack(pady=(0, 10))

        customtkinter.CTkLabel(self, text="Data de Início:").pack()
        self.entry_data_inicio = CTkDatePicker(self)
        self.entry_data_inicio.set_date_format("%d/%m/%Y")
        self.entry_data_inicio.set_allow_manual_input(True)
        self.entry_data_inicio.pack(pady=(0, 10))

        customtkinter.CTkLabel(self, text="Data de Fim:").pack()
        self.entry_data_fim = CTkDatePicker(self)
        self.entry_data_fim.set_date_format("%d/%m/%Y")
        self.entry_data_fim.set_allow_manual_input(True)
        self.entry_data_fim.pack(pady=(0, 10))

        customtkinter.CTkButton(self, text="Adicionar", command=self._adicionar_semestre).pack(pady=20)

    def _adicionar_semestre(self):
        nome = self.entry_nome.get().strip()
        data_inicio_str = self.entry_data_inicio.get_date()
        data_fim_str = self.entry_data_fim.get_date()

        # Verificações básicas
        if not nome:
            CTkMessagebox(title="Erro", message="Nome do semestre não pode ser vazio.", icon="cancel")
            return
        if not data_inicio_str or not data_fim_str:
            CTkMessagebox(title="Erro", message="Datas de início e fim devem ser preenchidas.", icon="cancel")
            return

        # Conversão e validação das datas
        try:
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
        except ValueError:
            CTkMessagebox(title="Erro", message="Formato de data inválido. Use dd/mm/aaaa.", icon="cancel")
            return

        if data_inicio > data_fim:
            CTkMessagebox(title="Erro", message="Data de fim deve ser posterior à data de início.", icon="cancel")
            return

        # Persistência segura
        try:
            SemestreService.criar(
                nome,
                data_inicio.strftime("%Y-%m-%d"),
                data_fim.strftime("%Y-%m-%d"),
                self.conexao
            )
        except NomeRepetidoError as e:
            CTkMessagebox(title="Erro", message=str(e), icon="cancel")
            return
        except Exception as e:
            CTkMessagebox(title="Erro", message="Erro ao salvar semestre no banco de dados.", icon="cancel")
            print(f"[ERRO] Falha na criação do semestre: {e}")
            return

        if self.callback_atualizacao:
            try:
                self.callback_atualizacao()
            except Exception as e:
                print(f"[Aviso] Callback falhou: {e}")

        self.destroy()