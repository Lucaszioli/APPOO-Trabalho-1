from app.utils.database import Database
from app.models.atividade import Atividade, Trabalho, TipoAtividadeEnum
from app.ui.views.pagina_inicial import PaginaInicial
from app.services.semestre_services import SemestreService
from app.services.disciplinas_services import DisciplinaService
from app.services.atividade_services import AtividadeService
from app.services.service_universal import ServiceUniversal

def main():
    # Inicializar o banco de dados e criar tabelas usando o script SQL
    db = Database(db_path="db.db")
    semestre_service = SemestreService(db_path="db.db")
    disciplina_service = DisciplinaService(db_path="db.db")
    atividade_service = AtividadeService(db_path="db.db")
    service = ServiceUniversal(semestre_service=semestre_service, disciplina_service=disciplina_service)
    app = PaginaInicial(db._conexao, service=service)

    app.mainloop()
    
if __name__ == "__main__":
    main()