from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from criar_banco import create_table

import uvicorn
import psycopg2

# Constantes
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "database-prova.cw2ougivdfds.us-east-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "postgres"

import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    print('Criando tabela...\n')
    # cria o banco de dados
    create_table()

    print('Tabela criada.')
    sys.exit(0)

# Conexão com o banco
con = psycopg2.connect(
    database= DB_NAME,
    user= DB_USER,
    password= DB_PASSWORD,
    host= DB_HOST,
    port= DB_PORT
)

# Criação do cursor
cur = con.cursor()
app = FastAPI()

#CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/notes")
def get_notes():
    cur.execute("SELECT * FROM minhas_notas;")
    notes = cur.fetchall()
    return {"data":notes}

@app.get("/get_note/{id}")
def get_note(id: int):
    cur.execute(f"SELECT * FROM minhas_notas WHERE id == {id};")
    note = cur.fetchone()
    return {"data":note}

@app.post("/create_note")
def create_user(data: dict = Body()):
    cur.execute(f"INSERT INTO minhas_notas (titulo, descricao) VALUES ('{data['titulo']}', '{data['descricao']}');")
    con.commit()
    return {"data": "Nota criada com sucesso!"}

@app.put("/update_note")
def update_user(data: dict = Body()):
    cur.execute(f"UPDATE minhas_notas SET titulo = '{data['titulo']}', descricao = '{data['descricao']}' WHERE id = {data['id']};")
    con.commit()
    return {"data": "Nota atualizada com sucesso!"}

@app.delete("/delete_note")
def delete_user(data: dict = Body()):
    cur.execute(f"DELETE FROM minhas_notas WHERE id = {data['id']};")
    con.commit()
    return {"data": "Nota deletada com sucesso!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)