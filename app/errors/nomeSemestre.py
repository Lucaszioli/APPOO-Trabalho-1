class NomeRepetidoError(Exception):
    def __init__(self, nome):
        super().__init__(f"Nome {nome} já está sendo utilizado")
        self.nome = nome