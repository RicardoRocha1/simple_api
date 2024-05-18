from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Atleta(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

atletas = [
    {"nome": "João", "cpf": "12345678900", "centro_treinamento": "CT A", "categoria": "Profissional"},
    {"nome": "Maria", "cpf": "98765432100", "centro_treinamento": "CT B", "categoria": "Amador"}
]

@app.get("/atletas", response_model=List[Atleta])
def get_atletas(nome: Optional[str] = None, cpf: Optional[str] = None):
    results = atletas
    if nome:
        results = [atleta for atleta in results if atleta["nome"] == nome]
    if cpf:
        results = [atleta for atleta in results if atleta["cpf"] == cpf]
    return results
@app.get("/atletas/detalhes", response_model=List[Atleta])
def get_atletas_detalhes():
    return [
        {"nome": atleta["nome"], "centro_treinamento": atleta["centro_treinamento"], "categoria": atleta["categoria"]}
        for atleta in atletas
    ]
from sqlalchemy.exc import IntegrityError

@app.post("/atletas")
def create_atleta(atleta: Atleta):
    try:
        add_atleta_to_db(atleta)
    except IntegrityError:
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")
    return atleta
from fastapi_pagination import Page, paginate, add_pagination

@app.get("/atletas/paginados", response_model=Page[Atleta])
def get_atletas_paginados():
    return paginate(atletas)

add_pagination(app)