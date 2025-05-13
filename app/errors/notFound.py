from abc import ABC, abstractmethod

class NotFoundError(Exception):
    @abstractmethod
    def __init__(self, message):
        super().__init__(message)

class SemestreNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(f"O Semestre não existe")

class DisciplinaNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(f"A Disciplina não existe")

class AtividadeNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(f"A Atividade não existe")