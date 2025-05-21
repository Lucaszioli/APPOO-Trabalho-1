from abc import ABC


class TipoAtividadeEnum:
    def __init__(self):
        self.TRABALHO = "Trabalho"
        self.PROVA = "Prova"
        self.CAMPO = "Aula de campo"
        self.REVISAO = "Aula de revisão"


class Atividade(ABC):
    def __init__(self, nome, data, disciplina_id, observacao = None, id=None, lugar = None, data_apresentacao = None, nota_total = None, nota = None, tipo = None):
        self.id = id
        self.nome = nome
        self.data = data
        self.disciplina_id = disciplina_id
        self.observacao = observacao
        self.lugar = lugar
        self.data_apresentacao = data_apresentacao
        self.nota_total = nota_total
        self.nota = nota
        self.tipo = tipo


class Trabalho(Atividade):
    def __init__(self, nome, data, disciplina_id, nota_total, data_apresentacao = None, nota = None, observacao = None, id=None):
        super().__init__(nome, data, disciplina_id, observacao, id, data_apresentacao=data_apresentacao, nota_total=nota_total, nota=nota)
        self.tipo = TipoAtividadeEnum().TRABALHO
        

class Prova(Atividade):
    def __init__(self, nome, data, disciplina_id, nota_total, nota = None, observacao = None, id=None):
        super().__init__(nome, data, disciplina_id, observacao, id, nota_total=nota_total, nota=nota)
        self.tipo = TipoAtividadeEnum().PROVA

class Aula_de_Campo(Atividade):
    def __init__(self, nome, data, disciplina_id, lugar, observacao = None, id=None):
        super().__init__(nome, data, disciplina_id, observacao, id, lugar=lugar)
        self.tipo = TipoAtividadeEnum().CAMPO


class Revisao(Atividade):
    def __init__(self, nome, data, disciplina_id, observacao = None, id=None):
        super().__init__(nome, data, disciplina_id, observacao, id)
        self.tipo = TipoAtividadeEnum().REVISAO
        