import customtkinter
from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
import logging

logger = logging.getLogger(__name__)

class BaseComponent(customtkinter.CTkFrame, ABC):
    """Componente base com funcionalidades comuns."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._setup_style()
        self._build_ui()
        
    def _setup_style(self):
        """Define estilos padrão do componente."""
        self.configure(
            corner_radius=8,
            fg_color=("gray95", "gray10")
        )
        
    @abstractmethod
    def _build_ui(self):
        """Constrói a interface do componente."""
        pass

class StyledButton(customtkinter.CTkButton):
    """Botão com estilos predefinidos."""
    
    STYLES = {
        'primary': {
            'fg_color': ("blue", "#1f538d"),
            'hover_color': ("lightblue", "#14375e"),
            'text_color': ("white", "white")
        },
        'secondary': {
            'fg_color': ("gray70", "gray30"),
            'hover_color': ("gray60", "gray40"),
            'text_color': ("black", "white")
        },
        'danger': {
            'fg_color': ("red", "#cc2936"),
            'hover_color': ("darkred", "#a02128"),
            'text_color': ("white", "white")
        },
        'success': {
            'fg_color': ("green", "#28a745"),
            'hover_color': ("darkgreen", "#1e7e34"),
            'text_color': ("white", "white")
        }
    }
    
    def __init__(self, master, style: str = 'primary', **kwargs):
        style_config = self.STYLES.get(style, self.STYLES['primary'])
        super().__init__(master, **{**style_config, **kwargs})

class StyledLabel(customtkinter.CTkLabel):
    """Label com estilos predefinidos."""
    
    def __init__(self, master, style: str = 'normal', **kwargs):
        styles = {
            'title': {'font': customtkinter.CTkFont(size=28, weight="bold")},
            'subtitle': {'font': customtkinter.CTkFont(size=18, weight="bold")},
            'heading': {'font': customtkinter.CTkFont(size=16, weight="bold")},
            'normal': {'font': customtkinter.CTkFont(size=14)},
            'small': {'font': customtkinter.CTkFont(size=12)},
            'caption': {'font': customtkinter.CTkFont(size=11, slant="italic")}
        }
        
        style_config = styles.get(style, styles['normal'])
        super().__init__(master, **{**style_config, **kwargs})

class StyledEntry(customtkinter.CTkEntry):
    """Entry com validação e estilos."""
    
    def __init__(self, master, placeholder: str = "", validator: Optional[Callable] = None, **kwargs):
        super().__init__(master, placeholder_text=placeholder, **kwargs)
        self.validator = validator
        self.configure(
            corner_radius=6,
            border_width=2,
            height=35
        )
        
        if validator:
            self.bind('<KeyRelease>', self._validate)
            
    def _validate(self, event=None):
        """Valida o conteúdo do campo."""
        if self.validator and self.get():
            is_valid = self.validator(self.get())
            color = ("green", "#28a745") if is_valid else ("red", "#dc3545")
            self.configure(border_color=color)

class Card(BaseComponent):
    """Componente de card para agrupar conteúdo."""
    
    def __init__(self, master, title: str = "", **kwargs):
        self.title = title
        super().__init__(master, **kwargs)
        
    def _build_ui(self):
        self.configure(
            corner_radius=12,
            border_width=1,
            border_color=("gray80", "gray25")
        )
        
        if self.title:
            title_label = StyledLabel(
                self, 
                text=self.title,
                style='heading',
                text_color=("gray10", "gray90")
            )
            title_label.pack(pady=(15, 10), padx=15, anchor="w")
            
        # Container para conteúdo
        self.content_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def add_content(self, widget):
        """Adiciona widget ao card."""
        widget.pack(in_=self.content_frame, pady=5, fill="x")
        return widget