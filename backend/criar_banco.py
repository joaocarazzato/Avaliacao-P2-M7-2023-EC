import psycopg2

# Constantes
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "database-prova.cw2ougivdfds.us-east-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "postgres"

def create_table():
    # Conexão com o banco
    con = psycopg2.connect(
        database= DB_NAME,
        user= DB_USER,
        password= DB_PASSWORD,
        host= DB_HOST,
        port= DB_PORT
    )

    print ("Connection: ", con.closed) 

    # Criação do cursor
    cur = con.cursor()

    # Roda o comando SQL
    cur.execute(
        """DROP TABLE IF EXISTS minhas_notas;

        CREATE TABLE minhas_notas (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            descricao TEXT NOT null,
            data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );"""
    )

    # Commita as mudanças para o banco
    con.commit()
    # Fecha a conexão
    con.close()

if __name__ == '__main__':
    create_table()