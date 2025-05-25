import customtkinter
from typing import Optional
import threading
import time

class LoadingSpinner(customtkinter.CTkFrame):
    """Componente de loading com spinner animado."""
    
    def __init__(self, master, message: str = "Carregando...", **kwargs):
        super().__init__(master, **kwargs)
        self.message = message
        self.is_spinning = False
        self._build_ui()
        
    def _build_ui(self):
        self.configure(
            fg_color=("gray95", "gray10"),
            corner_radius=10,
            border_width=1,
            border_color=("gray80", "gray25")
        )
        
        # Spinner
        self.spinner_label = customtkinter.CTkLabel(
            self,
            text="⏳",
            font=customtkinter.CTkFont(size=24)
        )
        self.spinner_label.pack(pady=(20, 10))
        
        # Mensagem
        self.message_label = customtkinter.CTkLabel(
            self,
            text=self.message,
            font=customtkinter.CTkFont(size=14)
        )
        self.message_label.pack(pady=(0, 20))
        
    def start_spinning(self):
        """Inicia a animação do spinner."""
        if not self.is_spinning:
            self.is_spinning = True
            self._animate()
            
    def stop_spinning(self):
        """Para a animação do spinner."""
        self.is_spinning = False
        
    def _animate(self):
        """Anima o spinner."""
        if not self.is_spinning:
            return
            
        current = self.spinner_label.cget("text")
        spinners = ["⏳", "⌛", "⏳", "⌛"]
        next_index = (spinners.index(current) + 1) % len(spinners)
        
        self.spinner_label.configure(text=spinners[next_index])
        self.after(500, self._animate)

class ProgressCard(customtkinter.CTkFrame):
    """Card de progresso para operações longas."""
    
    def __init__(self, master, title: str = "Progresso", **kwargs):
        super().__init__(master, **kwargs)
        self.title = title
        self._build_ui()
        
    def _build_ui(self):
        self.configure(
            fg_color=("gray95", "gray10"),
            corner_radius=12,
            border_width=1,
            border_color=("gray80", "gray25")
        )
        
        # Título
        title_label = customtkinter.CTkLabel(
            self,
            text=self.title,
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(15, 10), padx=15)
        
        # Barra de progresso
        self.progress_bar = customtkinter.CTkProgressBar(
            self,
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Label de status
        self.status_label = customtkinter.CTkLabel(
            self,
            text="Iniciando...",
            font=customtkinter.CTkFont(size=12)
        )
        self.status_label.pack(padx=15, pady=(0, 15))
        
    def update_progress(self, value: float, status: str = ""):
        """Atualiza o progresso (0.0 a 1.0)."""
        self.progress_bar.set(value)
        if status:
            self.status_label.configure(text=status)
            
    def set_complete(self):
        """Marca como completo."""
        self.progress_bar.set(1.0)
        self.status_label.configure(text="✅ Concluído!")

class NotificationToast(customtkinter.CTkToplevel):
    """Toast notification que aparece temporariamente."""
    
    def __init__(self, parent, message: str, type: str = "info", duration: int = 3000):
        super().__init__(parent)
        self.message = message
        self.type = type
        self.duration = duration
        
        self._setup_window()
        self._build_ui()
        self._schedule_close()
        
    def _setup_window(self):
        """Configura a janela do toast."""
        self.withdraw()  # Esconde inicialmente
        self.overrideredirect(True)  # Remove decorações
        self.attributes("-topmost", True)  # Sempre no topo
        
        # Posiciona no canto superior direito
        self.update_idletasks()
        width, height = 300, 80
        screen_width = self.winfo_screenwidth()
        x = screen_width - width - 20
        y = 20
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def _build_ui(self):
        """Constrói a UI do toast."""
        # Cores baseadas no tipo
        colors = {
            "info": ("blue", "#1f538d"),
            "success": ("green", "#28a745"),
            "warning": ("orange", "#fd7e14"),
            "error": ("red", "#dc3545")
        }
        
        color = colors.get(self.type, colors["info"])
        
        # Container principal
        container = customtkinter.CTkFrame(
            self,
            fg_color=color,
            corner_radius=10
        )
        container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Ícones
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        icon = icons.get(self.type, "ℹ️")
        
        # Label com ícone e mensagem
        label = customtkinter.CTkLabel(
            container,
            text=f"{icon} {self.message}",
            text_color="white",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            wraplength=250
        )
        label.pack(expand=True, padx=10, pady=10)
        
    def _schedule_close(self):
        """Agenda o fechamento automático."""
        self.deiconify()  # Mostra o toast
        self.after(self.duration, self.destroy)

class ConfirmationDialog(customtkinter.CTkToplevel):
    """Dialog de confirmação customizado."""
    
    def __init__(self, parent, title: str, message: str, 
                 confirm_text: str = "Confirmar", cancel_text: str = "Cancelar"):
        super().__init__(parent)
        
        self.result = None
        self.title_text = title
        self.message = message
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
        
        self._setup_window()
        self._build_ui()
        
    def _setup_window(self):
        """Configura a janela do dialog."""
        self.title(self.title_text)
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Centraliza
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 200
        y = (self.winfo_screenheight() // 2) - 100
        self.geometry(f"400x200+{x}+{y}")
        
        # Modal
        self.transient(self.master)
        self.grab_set()
        self.focus()
        
    def _build_ui(self):
        """Constrói a UI do dialog."""
        # Container principal
        main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mensagem
        message_label = customtkinter.CTkLabel(
            main_frame,
            text=self.message,
            font=customtkinter.CTkFont(size=14),
            wraplength=350,
            justify="center"
        )
        message_label.pack(expand=True, pady=(0, 20))
        
        # Botões
        buttons_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Botão cancelar
        cancel_btn = customtkinter.CTkButton(
            buttons_frame,
            text=self.cancel_text,
            command=self._on_cancel,
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        # Botão confirmar
        confirm_btn = customtkinter.CTkButton(
            buttons_frame,
            text=self.confirm_text,
            command=self._on_confirm,
            fg_color="red",
            hover_color="darkred"
        )
        confirm_btn.grid(row=0, column=1, sticky="ew")
        
    def _on_confirm(self):
        """Callback do botão confirmar."""
        self.result = True
        self.destroy()
        
    def _on_cancel(self):
        """Callback do botão cancelar."""
        self.result = False
        self.destroy()
        
    def get_result(self):
        """Retorna o resultado da confirmação."""
        self.wait_window()
        return self.result