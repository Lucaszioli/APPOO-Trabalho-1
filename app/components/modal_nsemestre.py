import customtkinter
from CTkMessagebox import CTkMessagebox
from app.components.date_picker import CTkDatePicker
from datetime import datetime

from app.services.semestre_services import SemestreService

class ModalNovoSemestre(customtkinter.CTkToplevel):
    def __init__(self, conexao, master=None, callback_atualizacao=None):
        super().__init__(master)
        self.conexao = conexao
        self.callback_atualizacao = callback_atualizacao
        self.title("Adicionar Novo Semestre")
        self.geometry("400x300")
        self._criar_widgets()

    def _criar_widgets(self):
        # Nome do Semestre
        label_nome = customtkinter.CTkLabel(self, text="Nome do Semestre:")
        label_nome.pack()

        self.entry_nome = customtkinter.CTkEntry(self)
        self.entry_nome.pack(pady=(0,10))
        
        # Data de Início
        label_data_inicio = customtkinter.CTkLabel(self, text="Data de Início:")
        label_data_inicio.pack()
        
        self.entry_data_inicio = CTkDatePicker(self)
        self.entry_data_inicio.set_date_format("%d/%m/%Y")
        self.entry_data_inicio.set_allow_manual_input(True)
        self.entry_data_inicio.pack(pady=(0,10))
        
        # Data de Fim
        label_data_fim = customtkinter.CTkLabel(self, text="Data de Fim:")
        label_data_fim.pack()
                
        self.entry_data_fim = CTkDatePicker(self)
        self.entry_data_fim.set_date_format("%d/%m/%Y")
        self.entry_data_fim.set_allow_manual_input(True)
        self.entry_data_fim.pack(pady=(0,10))

        # Botão Adicionar
        btn_adicionar = customtkinter.CTkButton(self, text="Adicionar", command=self._adicionar_semestre)
        btn_adicionar.pack(pady=20)

    def _adicionar_semestre(self):
        nome = self.entry_nome.get()
        data_inicio_str = self.entry_data_inicio.get_date()
        data_fim_str = self.entry_data_fim.get_date()

        # Verificação básica
        if not nome:
            CTkMessagebox(title="Erro", message="Nome do semestre não pode ser vazio!", icon="cancel")
            return
        if not data_inicio_str:
            CTkMessagebox(title="Erro", message="Data de início não pode ser vazia!", icon="cancel")
            return
        if not data_fim_str:
            CTkMessagebox(title="Erro", message="Data de fim não pode ser vazia!", icon="cancel")
            return

        # Validação de formato e ordem
        try:
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
        except ValueError:
            CTkMessagebox(title="Erro", message="Formato de data inválido! Use dd/mm/aaaa.", icon="cancel")
            return

        if data_inicio > data_fim:
            CTkMessagebox(title="Erro", message="A data de fim deve ser posterior à data de início.", icon="cancel")
            return

        # Persistência
        SemestreService.criar(
            nome,
            data_inicio.strftime("%Y-%m-%d"),
            data_fim.strftime("%Y-%m-%d"),
            self.conexao
        )

        if self.callback_atualizacao:
            self.callback_atualizacao()

        self.destroy()

