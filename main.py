from app.utils.database import Database
from app.models.atividade import Atividade, Trabalho

def main():
    # Inicializar o banco de dados e criar tabelas usando o script SQL
    db = Database(db_path="db.db")
    db.criar("app/scripts/init.sql")

    atividade = Trabalho("Trabalho de Matemática", "2023-10-15", 1, 5, 4, "Entregar até o dia 20")
    atividade.adicionar_bd(db.conectar())

    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    main()