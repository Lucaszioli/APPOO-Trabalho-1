from app.utils.database import Database
from abc import ABC, abstractmethod
class ServiceBase(Database, ABC):
    def __init__(self, db_path="db.db"):
        super().__init__(db_path)

    @abstractmethod
    def buscar_por_id(self, id:str):
        """Busca um objeto pelo ID."""
        pass
    
    @abstractmethod
    def listar(self):
        """Lista todos os objetos do tipo."""
        pass

    @abstractmethod
    def _adicionar_bd(self, obj):  
        """Adiciona um objeto ao banco de dados."""
        pass

    @abstractmethod
    def editar_bd(self, obj):
        """Edita um objeto no banco de dados."""
        pass

    @abstractmethod
    def deletar(self, obj):
        """Remove um objeto do banco de dados."""
        pass