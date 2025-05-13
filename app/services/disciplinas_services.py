from app.models.atividade import TipoAtividade, Trabalho, Aula_de_Campo, Prova, Revisao

class DisciplinaServices:
    @staticmethod
    def adicionar_bd(disciplina, conexao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO disciplina (nome, carga_horaria, semestre_id, codigo, observacao) VALUES (?, ?, ?, ?, ?)", (disciplina.nome, disciplina.carga_horaria, disciplina.semestre_id, disciplina.codigo, disciplina.observacao))
        conexao.commit()
        disciplina.id = cursor.lastrowid
    
    @staticmethod
    def editar_bd(disciplina, conexao):
        cursor = conexao.cursor()
        cursor.execute("UPDATE disciplina SET nome = ?, carga_horaria = ?, semestre_id = ?, observacao = ? WHERE id = ?", (disciplina.nome, disciplina.carga_horaria, disciplina.semestre_id, disciplina.observacao, disciplina.id))
        conexao.commit()
    
    @staticmethod
    def deletar_bd(disciplina, conexao):
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM disciplina WHERE id = ?", (disciplina.id,))
        conexao.commit()

    @staticmethod
    def carregar_atividades(disciplina, conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM atividade WHERE disciplina_id = ?", (disciplina.id,))
        atividades = cursor.fetchall()
        for atividade in atividades:
            if atividade[6] == TipoAtividade.TRABALHO.value:
                disciplina.atividades.append(Trabalho(atividade[1], atividade[2], atividade[3], atividade[5], atividade[6], atividade[7]))
            elif atividade[6] == TipoAtividade.PROVA.value:
                disciplina.atividades.append(Prova(atividade[1], atividade[2], atividade[3], atividade[5], atividade[6], atividade[7]))
            elif atividade[6] == TipoAtividade.CAMPO.value:
                disciplina.atividades.append(Aula_de_Campo(atividade[1], atividade[2], atividade[3], atividade[7]))
            elif atividade[6] == TipoAtividade.REVISAO.value:
                disciplina,atividade.append(Revisao(atividade[1], atividade[2], atividade[3], atividade[5], atividade[6], atividade[7]))
        return disciplina.atividades
    
    @staticmethod
    def criar(nome, carga_horaria, codigo,conexao, semestre, observacao = None):
        from app.models.disciplinas import Disciplina
        disciplina = Disciplina(nome, carga_horaria, semestre.id, codigo, observacao)
        DisciplinaServices.adicionar_bd(disciplina, conexao)
        semestre.adicionar_disciplina(disciplina)
        return disciplina
    
    @staticmethod
    def listar_disciplinas(semestre, conexao):
        from app.models.disciplinas import Disciplina
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM disciplina WHERE semestre_id = ?", (semestre.id,))
        disciplinas = cursor.fetchall()
        return [Disciplina(id=row[0], nome=row[1], carga_horaria=row[2], semestre_id=row[3], codigo=row[4], observacao=row[5]) for row in disciplinas]
        