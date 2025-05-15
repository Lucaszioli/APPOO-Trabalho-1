from app.utils.database import Database
from app.models.atividade import Atividade, Trabalho
from app.views.pagina_inicial import PaginaInicial
from app.services.semestre_services import SemestreService
from app.services.disciplinas_services import DisciplinaService
def main():
    # Inicializar o banco de dados e criar tabelas usando o script SQL
    db = Database(db_path="db.db")
    semestre_service = SemestreService(db_path="db.db")
    disciplina_service = DisciplinaService(db_path="db.db")
    app = PaginaInicial(db.conexao,semestre_service=semestre_service, disciplina_service=disciplina_service)
    app.mainloop()
    
if __name__ == "__main__":
    main()