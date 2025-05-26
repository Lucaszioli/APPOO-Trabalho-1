from abc import ABC, abstractmethod
import logging
import customtkinter
from CTkMessagebox import CTkMessagebox
from app.errors.nomeSemestre import NomeRepetidoError
from app.services.service_base import ServiceBase
from app.components.ui.base_components import StyledLabel, StyledEntry, StyledButton, Card
from typing import Type, Optional, Callable, Dict, Any

logger = logging.getLogger(__name__)

class ImprovedModal(customtkinter.CTkToplevel, ABC):
    """Modal melhorado com design responsivo e validação avançada."""
    
    def __init__(
        self,
        conexao,
        service: Type[ServiceBase],
        master=None,
        callback=None,
        title: str = "Modal",
        size: tuple[int, int] = (500, 500),
        item=None
    ):
        super().__init__(master)
        
        if conexao is None:
            CTkMessagebox(title="Erro", message="Conexão não fornecida.", icon="cancel")
            self.destroy()
            return
            
        self.conexao = conexao
        self.service = service
        self.callback = callback
        self.item = item
        self.fields: Dict[str, Any] = {}
        
        self._setup_window(title, size)
        self._build_ui()
        
    def _setup_window(self, title: str, size: tuple[int, int]):
        """Configura a janela do modal."""
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        
        # Centraliza na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (size[0] // 2)
        y = (self.winfo_screenheight() // 2) - (size[1] // 2)
        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        
        # Torna modal
        self.transient(self.master)
        self.grab_set()
        
        # Foco no modal
        self.focus()
        
    def _build_ui(self):
        """Constrói a interface do modal."""
        # Container principal
        main_container = customtkinter.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Card do conteúdo
        content_card = Card(main_container)
        content_card.pack(fill="both", expand=True)
        
        # Área do formulário
        self.form_frame = customtkinter.CTkFrame(
            content_card.content_frame,
            fg_color="transparent"
        )
        self.form_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        self._build_form()
        
        # Botões de ação
        self._build_action_buttons(content_card.content_frame)
        
    def _build_action_buttons(self, parent):
        """Cria os botões de ação."""
        buttons_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Botão cancelar
        cancel_btn = StyledButton(
            buttons_frame,
            text="Cancelar",
            style='secondary',
            command=self.destroy,
            height=40
        )
        cancel_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        # Botão salvar
        save_btn = StyledButton(
            buttons_frame,
            text="Salvar",
            style='success',
            command=self._on_submit,
            height=40
        )
        save_btn.grid(row=0, column=1, sticky="ew")
        
    def add_field(self, key: str, label: str, field_type: str = "entry", 
                  required: bool = True, validator: Optional[Callable] = None, **kwargs):
        """Adiciona um campo ao formulário."""
        # Label
        field_label = StyledLabel(
            self.form_frame,
            text=f"{label}{'*' if required else ''}:",
            style='normal'
        )
        field_label.pack(anchor="w", pady=(10, 5))
        
        # Campo
        if field_type == "entry":
            field = StyledEntry(
                self.form_frame,
                validator=validator,
                **kwargs
            )
        elif field_type == "textbox":
            field = customtkinter.CTkTextbox(
                self.form_frame,
                height=80,
                corner_radius=6,
                **kwargs
            )
        else:
            raise ValueError(f"Tipo de campo não suportado: {field_type}")
            
        field.pack(fill="x", pady=(0, 5))
        
        # Armazena referência
        self.fields[key] = {
            'widget': field,
            'required': required,
            'validator': validator,
            'type': field_type
        }
        
        return field
        
    def _on_submit(self):
        """Processa o envio do formulário."""
        # Coleta dados
        data = self._collect_data()
        
        # Valida
        is_valid, error_msg = self._validate_all(data)
        if not is_valid:
            self.grab_release()
            CTkMessagebox(title="Erro de Validação", message=error_msg, icon="cancel")
            return
            
        # Salva
        try:
            self._save(data)
        except NomeRepetidoError as e:
            logger.exception("Nome repetido")
            self.grab_release()
            CTkMessagebox(title="Erro", message=str(e), icon="cancel")
            return
        except Exception as e:
            logger.exception("Erro ao salvar")
            self.grab_release()
            CTkMessagebox(title="Erro", message=f"Falha ao salvar: {str(e)}", icon="cancel")
            return
            
        # Callback e fechar
        if self.callback:
            try:
                self.callback()
            except Exception:
                logger.warning("Callback falhou")
                
        self.destroy()
        
    def _collect_data(self) -> dict:
        """Coleta dados de todos os campos."""
        data = {}
        for key, field_info in self.fields.items():
            widget = field_info['widget']
            field_type = field_info['type']
            
            if field_type == "entry":
                data[key] = widget.get().strip()
            elif field_type == "textbox":
                data[key] = widget.get("1.0", "end-1c").strip()
                
        return data
        
    def _validate_all(self, data: dict) -> tuple[bool, str]:
        """Valida todos os campos."""
        # Campos obrigatórios
        for key, field_info in self.fields.items():
            if field_info['required'] and not data.get(key):
                return False, f"Campo obrigatório não preenchido."
                
            # Validador customizado
            if field_info['validator'] and data.get(key):
                if not field_info['validator'](data[key]):
                    return False, f"Valor inválido no campo."
                    
        # Validação customizada
        return self._validate_custom(data)
        
    def _validate_custom(self, data: dict) -> tuple[bool, str]:
        """Validação customizada. Pode ser sobrescrita."""
        return True, ""
        
    @abstractmethod
    def _build_form(self):
        """Constrói o formulário. Deve ser implementado pelas subclasses."""
        pass
        
    @abstractmethod
    def _save(self, data: dict):
        """Salva os dados. Deve ser implementado pelas subclasses."""
        pass