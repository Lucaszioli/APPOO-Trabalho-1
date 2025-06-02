class incorrectDate(Exception):
    def __init__(self, data, msg="Data inválida"):
        """Exceção para data inválida."""
        super().__init__(msg)
        self.data = data