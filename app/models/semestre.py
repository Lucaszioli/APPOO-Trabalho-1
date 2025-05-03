from .disciplinas import Disciplina

class Semestre:
    def __init__(self, nome, data_inicio, data_fim, id=None):
        self.id = id
        self.nome = nome
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.disciplinas = []

    def adicionar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO semestre (nome, data_inicio, data_fim) VALUES (?, ?, ?)", (self.nome, self.data_inicio, self.data_fim))
        conexao.commit()
        self.id = cursor.lastrowid

    def adicionar_disciplina(self, disciplina):
        self.disciplinas.append(disciplina)

    def editar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("UPDATE semestre SET nome = ?, data_inicio = ?, data_fim = ? WHERE id_semestre = ?", (self.nome, self.data_inicio, self.data_fim, self.id_semestre))
        conexao.commit()
    
    def deletar_bd(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM semestre WHERE id_semestre = ?", (self.id_semestre,))
        conexao.commit()
    
    
    @staticmethod
    def listar_semestres(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM semestre")
        semestres = cursor.fetchall()
        return [Semestre(id_semestre=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3]) for row in semestres]
    
    @staticmethod
    def buscar_ultimo_semestre(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM semestre ORDER BY data_fim DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            return Semestre(id_semestre=row[0], nome=row[1], data_inicio=row[2], data_fim=row[3])
        return None
    
    def carregar_disciplinas(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM disciplina WHERE semestre_id = ?", (self.id_semestre,))
        disciplinas = cursor.fetchall()
        for disciplina in disciplinas:
            self.disciplinas.append(Disciplina(nome=disciplina[1], carga_horaria=disciplina[2], semestre_id=disciplina[3], codigo=disciplina[4], observacao=disciplina[5], id=disciplina[0]))

    def listar_disciplinas(self):
        for disciplina in self.disciplinas:
            print(f"Disciplina: {disciplina.nome}, Carga Horária: {disciplina.carga_horaria}, Código: {disciplina.codigo}, Observação: {disciplina.observacao}")