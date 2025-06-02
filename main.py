from app.utils.database import Database
from app.models.atividade import Atividade, Trabalho, TipoAtividadeEnum
from app.ui.views.pagina_inicial import PaginaInicial
from app.services.semestre_services import SemestreService
from app.services.disciplinas_services import DisciplinaService
from app.services.atividade_services import AtividadeService
from app.services.service_universal import ServiceUniversal

def main():
    db = Database(db_path="db.db")
    service = ServiceUniversal(db_path="db.db")
    app = PaginaInicial(service=service)

    app.mainloop()
    
if __name__ == "__main__":
    main()