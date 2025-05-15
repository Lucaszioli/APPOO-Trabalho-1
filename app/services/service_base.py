from app.utils.database import Database
from abc import ABC, abstractmethod
class ServiceBase(Database, ABC):
    def __init__(self, db_path="db.db"):
        super().__init__(db_path)

    @abstractmethod
    def buscar_por_id(self, id:str):
        pass
    
    @abstractmethod
    def listar(self):
        pass