class Disciplina:
    def __init__(self, nome, carga_horaria, semestre_id, codigo, observacao = None, id = None):
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.semestre_id = semestre_id
        self.atividades = []
        self.codigo = codigo
        self.observacao = observacao
        self.id = id

    def adicionar_atividade(self, atividade):
        self.atividades.append(atividade)

    def listar_atividades(self):
        for atividade in self.atividades:
            print(f"Atividade: {atividade.nome}, Data: {atividade.data}, Nota Total: {atividade.nota_total}, Observação: {atividade.observacao}")
    
    
    