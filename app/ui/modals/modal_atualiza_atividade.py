from typing import Any, Optional, Callable
from app.ui.components.components_base import StyledEntry
from app.ui.modals.modal_base import ModalBase
from app.models.atividade import Atividade
from app.services.service_universal import ServiceUniversal
from app.ui.components.date_picker import CTkDatePicker
from datetime import datetime
from CTkMessagebox import CTkMessagebox
import customtkinter

class ModalAtualizaAtividade(ModalBase):
    """Modal para atualização de uma atividade."""

    def __init__(
        self,
        disciplina: Any = None,
        conexao: Any = None,
        service: ServiceUniversal = None,
        master: Optional[Any] = None,
        callback: Optional[Callable] = None,
        item: Optional[Any] = None
    ):
        self.disciplina = disciplina
        self.item = item
        super().__init__(
            conexao=conexao,
            service=service,
            master=master,
            callback=callback,
            title="Editar Atividade",
            size=(600, 600),
            item=item
        )

    def _to_br_format(self, date_str):
        """Convert date string to Brazilian format."""
        from datetime import datetime
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return date_str
        except Exception:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
            except Exception:
                return date_str

    def _build_form(self) -> None:
        """Build the form with dynamic fields based on activity type."""
        atividade = self.item
        
        # Nome da atividade
        nome_field = self.add_field(
            key="nome",
            label="Nome da Atividade",
            required=True,
            placeholder="Ex: Prova Final"
        )
        nome_field.insert(0, getattr(atividade, "nome", ""))
        
        # Tipo de atividade com callback para mudanças dinâmicas
        self.type = self.add_field(
            key="tipo",
            label="Tipo de Atividade",
            required=True,
            field_type="combobox",
            values=["Trabalho", "Prova", "Aula de campo", "Aula de revisão"],
            command=self._on_type_change
        )
        self.type.set(getattr(atividade, "tipo", ""))
        
        # Data da atividade
        dates_container = customtkinter.CTkFrame(self.form_frame, fg_color="transparent")
        dates_container.pack(fill="x", pady=10)
        dates_container.grid_columnconfigure((0, 1), weight=1)
        data_label = customtkinter.CTkLabel(
            dates_container,
            text="Data da Atividade*:",
            font=customtkinter.CTkFont(size=14)
        )
        data_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        data_val = getattr(atividade, "data", "")
        data_placeholder = self._to_br_format(data_val) if data_val else "Ex: 27/05/2025"
        self.date_picker = CTkDatePicker(dates_container, placeholder=data_placeholder)
        self.date_picker.set_date_format("%d/%m/%Y")
        self.date_picker.set_allow_manual_input(False)
        if data_val:
            self.date_picker.insert(self._to_br_format(data_val))
        self.date_picker.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        
        # Container para campos dinâmicos
        self.dynamic_container = customtkinter.CTkFrame(self.form_frame, fg_color="transparent")
        self._update_dynamic_fields(self.type.get())
        
        # Observações
        observacao_field = self.add_field(
            key="observacao",
            label="Observações",
            field_type="textbox",
            required=False
        )
        observacao_field.insert("1.0", getattr(atividade, "observacao", ""))
        
        # Progresso
        progresso_field = self.add_field(
            key="progresso",
            label="Progresso",
            field_type="combobox",
            values=["Não começou", "Em andamento", "Concluída", "Entregue"],
            required=True,
            default="Não começou"
        )
        progresso_field.set(getattr(atividade, "progresso", "Não começou"))

    def _on_type_change(self, value):
        """Handle activity type changes and update dynamic fields."""
        self._update_dynamic_fields(value)
    
    def _update_dynamic_fields(self, tipo) -> None:
        """Update dynamic fields based on activity type."""
        # Clear existing dynamic fields
        for widget in self.dynamic_container.winfo_children():
            widget.destroy()
        
        # Reset dynamic field references - Corrigido: mais completo
        for attr in ['data_apresentacao_picker', 'local_entry', 'materia_entry', 'pontuacao_entry', 'nota_entry']:
            if hasattr(self, attr):
                setattr(self, attr, None)
        
        # Remove dynamic fields from form validation
        for key in ["pontuacao", "nota", "data_apresentacao", "local", "materia"]:
            if key in self.fields:
                del self.fields[key]

        atividade = self.item
        
        # Add grade field for Prova/Trabalho
        if tipo in ("Prova", "Trabalho"):
            nota_label = customtkinter.CTkLabel(
                self.dynamic_container,
                text="Nota Obtida:",
                font=customtkinter.CTkFont(size=14)
            )
            nota_label.pack(anchor="w", padx=(0, 10))
            self.nota_entry = StyledEntry(
                self.dynamic_container,
                placeholder="Ex: 8.5",
                validator=lambda value: value == '' or (value.replace('.', '', 1).isdigit() and float(value) >= 0),  # Corrigido: permite vazio
            )
            self.nota_entry.pack(fill="x", padx=(0, 10))
            # Pre-fill existing grade
            if hasattr(atividade, 'nota') and atividade.nota is not None:
                self.nota_entry.insert(0, str(atividade.nota))
            
            self.fields["nota"] = {
                'widget': self.nota_entry,
                'required': False,
                'validator': lambda value: value == '' or (value.replace('.', '', 1).isdigit() and float(value) >= 0),
                'type': "entry"
            }

        # Type-specific fields
        if tipo in ("Prova", "Trabalho"):
            self.dynamic_container.pack(fill="x", pady=10)
            label = customtkinter.CTkLabel(
                self.dynamic_container,
                text="Pontuação Máxima*",
                font=customtkinter.CTkFont(size=14)
            )
            label.pack(anchor="w", padx=(0, 10))
            self.pontuacao_entry = StyledEntry(
                self.dynamic_container,
                placeholder="Ex: 10",
                validator=lambda value: value.replace('.', '', 1).isdigit() and float(value) > 0,
            )
            self.pontuacao_entry.pack(fill="x", padx=(0, 10))
            # Pre-fill existing pontuacao/nota_total
            if hasattr(atividade, 'nota_total') and atividade.nota_total is not None:
                self.pontuacao_entry.insert(0, str(atividade.nota_total))
            elif hasattr(atividade, 'pontuacao') and atividade.pontuacao is not None:
                self.pontuacao_entry.insert(0, str(atividade.pontuacao))
            
            self.fields["pontuacao"] = {
                'widget': self.pontuacao_entry,
                'required': True,
                'validator': lambda value: value.replace('.', '', 1).isdigit() and float(value) > 0,   
                'type': "entry"
            }

        elif tipo == "Trabalho":
            self.dynamic_container.pack(fill="x", pady=10)
            label = customtkinter.CTkLabel(
                self.dynamic_container,
                text="Data de Apresentação:",
                font=customtkinter.CTkFont(size=14)
            )
            label.pack(anchor="w", padx=(0, 10))
            
            # Importação corrigida
            from app.ui.components.date_picker import CTkDatePicker
            
            self.data_apresentacao_picker = CTkDatePicker(
                self.dynamic_container,
                placeholder="Ex: 25/12/2024"
            )
            self.data_apresentacao_picker.set_date_format("%d/%m/%Y")
            self.data_apresentacao_picker.set_allow_manual_input(True)
            # Pre-fill existing data_apresentacao
            if hasattr(atividade, 'data_apresentacao') and atividade.data_apresentacao:
                if isinstance(atividade.data_apresentacao, str):
                    self.data_apresentacao_picker.insert(self._to_br_format(atividade.data_apresentacao))
            self.data_apresentacao_picker.pack(fill="x", padx=(0, 10))

        elif tipo == "Aula de campo":
            self.dynamic_container.pack(fill="x", pady=10)
            label = customtkinter.CTkLabel(
                self.dynamic_container,
                text="Local da Atividade:",
                font=customtkinter.CTkFont(size=14)
            )
            label.pack(anchor="w", padx=(0, 10))
            self.local_entry = customtkinter.CTkEntry(
                self.dynamic_container,
                placeholder_text="Ex: Parque Nacional",
            )
            self.local_entry.pack(fill="x", padx=(0, 10))
            # Pre-fill existing lugar
            if hasattr(atividade, 'lugar') and atividade.lugar:
                self.local_entry.insert(0, atividade.lugar)

        elif tipo == "Aula de revisão":
            self.dynamic_container.pack(fill="x", pady=10)
            label = customtkinter.CTkLabel(
                self.dynamic_container,
                text="Matéria da Revisão:",
                font=customtkinter.CTkFont(size=14)
            )
            label.pack(anchor="w", padx=(0, 10))
            self.materia_entry = customtkinter.CTkEntry(
                self.dynamic_container,
                placeholder_text="Capitulo 1, Livro X",
            )
            self.materia_entry.pack(fill="x", padx=(0, 10))
            # Pre-fill existing materia
            if hasattr(atividade, 'materia') and atividade.materia:
                self.materia_entry.insert(0, atividade.materia)
        
        # Força atualização visual
        self.dynamic_container.update_idletasks()

    def _validate_data(self, value: str) -> bool:
        """Validate date format and value."""
        try:
            day, month, year = map(int, value.split('/'))
            datetime(year, month, day)
        except ValueError:
            CTkMessagebox(title="Erro", message="Data inválida. Use o formato DD/MM/AAAA.", icon="cancel")
            return False
        return True

    def _validate_custom(self, data: dict) -> tuple[bool, str]:
        """Validate custom fields before saving."""
        if not data["nome"]:
            return False, "O nome da atividade é obrigatório."
        if not data["data"]:
            return False, "A data da atividade é obrigatória."
        if not data["tipo"]:
            return False, "O tipo da atividade é obrigatório."
        
        # Validate type-specific fields
        if data["tipo"] in ("Prova", "Trabalho"):
            if not data.get("pontuacao") or not data["pontuacao"].replace('.', '', 1).isdigit() or float(data["pontuacao"]) <= 0:
                return False, "A pontuação deve ser um número positivo."
        
        # Validate presentation date for Trabalho
        try:
            if data["tipo"] == "Trabalho" and isinstance(data.get("data_apresentacao"), str) and data["data_apresentacao"]:
                apresentacao = datetime.strptime(data["data_apresentacao"], "%d/%m/%Y")
                entrega = datetime.strptime(data["data"], "%d/%m/%Y")
                if apresentacao < entrega:
                    return False, "A data de apresentação não pode ser anterior à data da atividade."
        except ValueError:
            return False, "Formato de data inválido para a apresentação."
        
        return True, ""

    def _save(self, data: dict) -> None:
        """Save the updated activity to the database."""
        try:
            atividade = self.item
            
            # Temporarily allow tipo updates for this editing session
            atividade._allow_tipo_update = True
            
            atividade.nome = data["nome"]
            atividade.data = data["data"]
            atividade.tipo = data["tipo"]
            atividade.observacao = data.get("observacao", "")
            atividade.progresso = data.get("progresso", "Não começou")
            
            # Handle type-specific fields
            if data["tipo"] in ("Prova", "Trabalho"):
                atividade.nota_total = float(data["pontuacao"]) if data.get("pontuacao") not in (None, "") else None
                atividade.pontuacao = float(data["pontuacao"]) if data.get("pontuacao") not in (None, "") else None
                atividade.nota = float(data["nota"]) if data.get("nota") not in (None, "") else None
            
            if data["tipo"] == "Trabalho":
                atividade.data_apresentacao = data.get("data_apresentacao", None)
            
            if data["tipo"] == "Aula de campo":
                atividade.lugar = data.get("local", None)
            
            if data["tipo"] == "Aula de revisão":
                atividade.materia = data.get("materia", None)
            
            # Ensure expected attributes for editar_bd
            for attr in ["disciplina_id", "lugar", "data_apresentacao", "materia"]:
                if not hasattr(atividade, attr):
                    setattr(atividade, attr, None)
            
            self.service.atividade_service.editar_bd(atividade)
            
            # Clean up the temporary flag
            if hasattr(atividade, '_allow_tipo_update'):
                delattr(atividade, '_allow_tipo_update')
            
            if self.callback:
                self.callback()
            self.destroy()
        except Exception as e:
            # Clean up the temporary flag in case of error
            if hasattr(self.item, '_allow_tipo_update'):
                delattr(self.item, '_allow_tipo_update')
            CTkMessagebox(title="Erro", message=f"Não foi possível atualizar a atividade: {str(e)}", icon="cancel")

    def _collect_data(self) -> dict:
        """Collect form data including dynamic fields."""
        data = super()._collect_data()
        data["data"] = self.date_picker.get_date()
        
        tipo = self.type.get()
        
        # Collect type-specific data
        if tipo in ("Prova", "Trabalho"):
            data["pontuacao"] = self.pontuacao_entry.get() if self.pontuacao_entry else ""
            if hasattr(self, 'nota_entry') and self.nota_entry:
                data["nota"] = self.nota_entry.get()
            
        if tipo == "Trabalho" and hasattr(self, 'data_apresentacao_picker') and self.data_apresentacao_picker:
            data["data_apresentacao"] = self.data_apresentacao_picker.get_date()
        
        if tipo == "Aula de campo" and hasattr(self, 'local_entry') and self.local_entry:
            data["local"] = self.local_entry.get()
        
        if tipo == "Aula de revisão" and hasattr(self, 'materia_entry') and self.materia_entry:
            data["materia"] = self.materia_entry.get()
        
        data["progresso"] = self.fields["progresso"]["widget"].get() if "progresso" in self.fields else "Não começou"
        return data
