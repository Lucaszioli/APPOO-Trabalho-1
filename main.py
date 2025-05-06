from app.utils.database import Database
from app.models.atividade import Atividade, Trabalho
from app.views.pagina_inicial import PaginaInicial
from app.services.semestre_services import SemestreService
from app.services.disciplinas_services import DisciplinaServices
def main():
    # Inicializar o banco de dados e criar tabelas usando o script SQL
    db = Database(db_path="db.db")
    db.criar("app/scripts/init.sql")
    conexao = db.conectar()
    semestre = SemestreService.criar("Teste", "Inicio", "Fim", conexao )
    DisciplinaServices.criar(nome="Teste1", semestre_id=semestre.id,codigo="MAT60", carga_horaria=60, conexao=conexao)
    DisciplinaServices.criar(nome="Teste1", semestre_id=semestre.id,codigo="MAT61", carga_horaria=60, conexao=conexao)
    semestre.carregar_disciplinas(conexao)
    semestre.listar_disciplinas()
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    main()
    app = PaginaInicial()
    app.mainloop()