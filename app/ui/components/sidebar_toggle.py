import logging
import customtkinter
from CTkMessagebox import CTkMessagebox
from typing import Any
from app.ui.components.components_base import StyledButton, StyledLabel, Card

logger = logging.getLogger(__name__)

class SidebarToggle(customtkinter.CTkFrame):
    """Componente melhorado que gerencia a sidebar de configurações."""
    
    APPEARANCE_OPTIONS = ["Claro", "Escuro", "Sistema"]
    THEME_OPTIONS = ["Azul", "Verde", "Azul Escuro", "Rosa", "Violeta", "Vaporwave"]
    SCALING_OPTIONS = ["80%", "90%", "100%", "110%", "120%"]

    def __init__(
        self,
        master: customtkinter.CTk,
        controller: Any,
        *args,
        **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.sidebar: customtkinter.CTkFrame = None
        
        # Inicializa estado do botão de voltar
        self._show_back_button = False
        self._back_callback = None
        self._back_btn = None
        
        self._setup_style()
        self._create_toggle_button()

    def _setup_style(self):
        """Configura o estilo do componente."""
        self.configure(
            fg_color="transparent",
            corner_radius=0
        )

    def _create_toggle_button(self):
        """Cria o botão de toggle da sidebar."""
        self.open_button = StyledButton(
            self,
            text="☰",  # Ícone de hambúrguer mais moderno
            width=50,
            height=50,
            style='primary',
            command=self._toggle_sidebar,
            font=customtkinter.CTkFont(size=18, weight="bold"),
            corner_radius=10
        )
        self.open_button.pack(padx=15, pady=15)

    def _toggle_sidebar(self) -> None:
        """Alterna entre abrir e fechar a sidebar."""
        if self.sidebar and self.sidebar.winfo_exists():
            self._close_sidebar()
        else:
            self._open_sidebar()

    def _open_sidebar(self) -> None:
        """Abre a sidebar com configurações."""
        if self.sidebar and self.sidebar.winfo_exists():
            return
            
        try:
            self._create_sidebar()
            # Usa o estado salvo para mostrar o botão de voltar
            show_back = getattr(self, '_show_back_button', False)
            back_callback = getattr(self, '_back_callback', None)
            self._add_options(show_back_button=show_back, back_callback=back_callback)
        except Exception:
            logger.exception("Falha ao abrir sidebar")
            CTkMessagebox(
                title="Erro", 
                message="Não foi possível abrir o menu de configurações.", 
                icon="cancel"
            )

    def _create_sidebar(self) -> None:
        """Cria a estrutura da sidebar."""
        self.sidebar = customtkinter.CTkFrame(
            self.master, 
            width=280,
            corner_radius=0,
            fg_color=("gray90", "gray20")
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_columnconfigure(0, weight=1)
        
        # Reserva espaço para todas as seções incluindo o botão de voltar opcional
        for i in range(8):  # 0: back_btn, 1: header, 2-6: options, 7: spacer
            self.sidebar.grid_rowconfigure(i, weight=0)
        self.sidebar.grid_rowconfigure(7, weight=1)  # Spacer que expande
        
        # Cabeçalho da sidebar (sempre na linha 1)
        header_card = Card(self.sidebar, title="⚙️ Configurações")
        header_card.grid(row=1, column=0, sticky="ew", padx=15, pady=(15, 10))
        close_btn = StyledButton(
            header_card.content_frame,
            text="✕ Fechar",
            style='secondary',
            command=self._close_sidebar,
            height=35
        )
        close_btn.pack(fill="x", pady=5)

    def _close_sidebar(self) -> None:
        """Fecha a sidebar."""
        if self.sidebar:
            self.sidebar.grid_forget()
            self.sidebar.destroy()
            self.sidebar = None

    def _add_options(self, show_back_button=False, back_callback=None) -> None:
        """Adiciona as opções de configuração à sidebar."""
        # Botão de voltar no topo (linha 0), se necessário
        if hasattr(self, '_back_btn') and self._back_btn:
            self._back_btn.destroy()
            self._back_btn = None
            
        if show_back_button and back_callback:
            self._back_btn = StyledButton(
                self.sidebar,
                text="← Voltar",
                style='secondary',
                command=back_callback,
                height=40
            )
            self._back_btn.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        
        # Card de Aparência (linha 2)
        appearance_card = Card(self.sidebar, title="Aparência")
        appearance_card.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        
        self._add_appearance_option(appearance_card.content_frame)
        
        # Card de Tema (linha 3)
        theme_card = Card(self.sidebar, title="Tema de Cores")
        theme_card.grid(row=3, column=0, sticky="ew", padx=15, pady=5)
        
        self._add_theme_option(theme_card.content_frame)
        
        # Card de Escala (linha 4)
        scale_card = Card(self.sidebar, title="Escala da Interface")
        scale_card.grid(row=4, column=0, sticky="ew", padx=15, pady=5)
        
        self._add_scale_option(scale_card.content_frame)
        
        # Card de Informações (linha 5)
        info_card = Card(self.sidebar, title="Sobre")
        info_card.grid(row=5, column=0, sticky="ew", padx=15, pady=5)
        
        self._add_info_section(info_card.content_frame)
        
        # Espaçador (linha 7)
        spacer = customtkinter.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.grid(row=7, column=0, sticky="ew")

    def _add_appearance_option(self, parent):
        """Adiciona opção de aparência."""
        desc_label = StyledLabel(
            parent,
            text="Escolha entre modo claro, escuro ou automático",
            style='small',
            wraplength=220
        )
        desc_label.pack(anchor="w", pady=(0, 10))
        
        appearance_menu = customtkinter.CTkOptionMenu(
            parent,
            values=self.APPEARANCE_OPTIONS,
            variable=self.controller.selected_appearance,
            command=self.controller.change_appearance_mode_event,
            height=35,
            corner_radius=8
        )
        appearance_menu.pack(fill="x", pady=(0, 5))

    def _add_theme_option(self, parent):
        """Adiciona opção de tema."""
        desc_label = StyledLabel(
            parent,
            text="Personalize as cores da interface",
            style='small',
            wraplength=220
        )
        desc_label.pack(anchor="w", pady=(0, 10))
        
        theme_menu = customtkinter.CTkOptionMenu(
            parent,
            values=self.THEME_OPTIONS,
            variable=self.controller.selected_theme,
            command=self.controller.change_theme_mode_event,
            height=35,
            corner_radius=8
        )
        theme_menu.pack(fill="x", pady=(0, 5))

    def _add_scale_option(self, parent):
        """Adiciona opção de escala."""
        desc_label = StyledLabel(
            parent,
            text="Ajuste o tamanho dos elementos da interface",
            style='small',
            wraplength=220
        )
        desc_label.pack(anchor="w", pady=(0, 10))
        
        scale_menu = customtkinter.CTkOptionMenu(
            parent,
            values=self.SCALING_OPTIONS,
            variable=self.controller.selected_scaling,
            command=self.controller.change_scaling_event,
            height=35,
            corner_radius=8
        )
        scale_menu.pack(fill="x", pady=(0, 5))

    def _add_info_section(self, parent):
        """Adiciona seção de informações."""
        info_text = """Sistema de Gerenciamento Acadêmico

Versão: 1.0
Desenvolvido com CustomTkinter

Funcionalidades:
• Gerenciamento de semestres
• Controle de disciplinas
• Interface moderna e responsiva"""
        
        info_label = StyledLabel(
            parent,
            text=info_text,
            style='small',
            justify="left",
            wraplength=220
        )
        info_label.pack(anchor="w")

    def set_back_button(self, show: bool, callback):
        """Define se o botão de voltar deve ser mostrado na sidebar."""
        self._show_back_button = show
        self._back_callback = callback
        
        # Se a sidebar estiver aberta, atualiza apenas o botão de voltar
        if hasattr(self, 'sidebar') and self.sidebar and self.sidebar.winfo_exists():
            # Remove o botão existente se houver
            if hasattr(self, '_back_btn') and self._back_btn:
                self._back_btn.destroy()
                self._back_btn = None
            
            # Adiciona o novo botão se necessário
            if show and callback:
                self._back_btn = StyledButton(
                    self.sidebar,
                    text="← Voltar",
                    style='secondary',
                    command=callback,
                    height=40
                )
                self._back_btn.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))

