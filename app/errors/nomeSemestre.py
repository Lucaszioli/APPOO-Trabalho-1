class NomeRepetidoError(Exception):
    def __init__(self, nome):
        """Exceção para nome de semestre já existente."""
        super().__init__(f"Nome {nome} já está sendo utilizado")
        self.nome = nome