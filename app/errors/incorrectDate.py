class incorrectDate(Exception):
    def __init__(self, data, msg="Data inválida"):
        super().__init__(msg)
        self.data = data