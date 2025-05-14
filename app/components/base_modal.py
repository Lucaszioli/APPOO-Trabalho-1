from abc import ABC, abstractmethod
import logging
import customtkinter
from CTkMessagebox import CTkMessagebox
from app.services.semestre_services import SemestreService
from app.errors.nomeSemestre import NomeRepetidoError
logger = logging.getLogger(__name__)

class BaseModal(customtkinter.CTkToplevel, ABC):
    """Modal genérico com fluxo comum de coleta, validação e salvamento."""
    def __init__(
        self,
        conexao,
        semestre_service:"SemestreService",
        master=None,
        callback=None,
        title: str = "Modal",
        size: tuple[int, int] = (400, 300),
        item=None
    ):
        super().__init__(master)
        if conexao is None:
            CTkMessagebox(title="Erro", message="Conexão não fornecida.", icon="cancel")
            self.destroy()
            return
        self.conexao = conexao
        self.semestre_service = semestre_service
        self.callback = callback
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self._build_widgets()

    @abstractmethod
    def _build_widgets(self): ...  # cria campos e botão submit

    def _on_submit(self):
        data = self._collect_data()
        valid, msg = self._validate(data)
        if not valid:
            CTkMessagebox(title="Erro", message=msg, icon="cancel")
            return
        try:
            self._save(data)
        except NomeRepetidoError as e:
            logger.exception("Nome de semestre repetido")
            CTkMessagebox(title="Erro", message=str(e), icon="cancel")
        except Exception:
            logger.exception("Erro ao salvar")
            CTkMessagebox(title="Erro", message="Falha ao salvar.", icon="cancel")
            return
        if self.callback:
            try:
                self.callback()
            except Exception:
                logger.warning("Callback falhou")
        self.destroy()

    @abstractmethod
    def _collect_data(self): ...  # retorna dict de valores

    @abstractmethod
    def _validate(self, data) -> tuple[bool, str]: ...  # valida e retorna (sucesso, mensagem)

    @abstractmethod
    def _save(self, data): ...  # persiste via serviço