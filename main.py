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

    app = PaginaInicial(conexao)
    app.mainloop()
    
if __name__ == "__main__":
    main()