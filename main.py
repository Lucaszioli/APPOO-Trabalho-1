from app.utils.database import Database

def main():
    # Inicializar o banco de dados e criar tabelas usando o script SQL
    db = Database(db_path="db.db")
    db.criar("app/scripts/init.sql")

    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    main()