import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

connection_str = os.getenv("DATABASE_CONNECTION")
client: MongoClient
try:
    client = MongoClient(connection_str)
except Exception:
    print("Erro " + Exception)
else:
    print("Conectado ao Mongo")


db = client.fastapi

# ----------------------- Funções para CRUD -----------------------
class Mongo:
    # ---------------------- Funções para Create ----------------------
    def inserir_varios_na_colecao(nome_colecao: str, objs: list):
        colecao = db.get_collection(nome_colecao)
        colecao.insert_many(objs)

    def inserir_na_colecao(nome_colecao: str, obj: dict):
        colecao = db.get_collection(nome_colecao)
        x = colecao.insert_one(obj)
        return x

    # ---------------------- Funções para Read ------------------------
    def buscar_varios_na_colecao(nome_colecao: str):
        colecao = db.get_collection(nome_colecao)
        dados = colecao.find()

        resultado = []

        for dado in dados:
            resultado.append(dado)

        return resultado

    def buscar_um_na_colecao(nome_colecao: str, obj: dict):
        colecao = db.get_collection(nome_colecao)
        res = colecao.find_one(obj)
        return res

    # ---------------------- Funções para Update ----------------------
    def atualizar_um_na_colecao(nome_colecao: str, filter: dict, novos_dados: dict):
        """Atualiza os dados do objeto de acordo com os novos dados

        usuario = {
            "id": id
        }

        novos_dados = {
            "$set": {"Nome_Campo": "Novo_Valor},
        }

        """
        colecao = db.get_collection(nome_colecao)
        colecao.update_one(filter, novos_dados)

    # ---------------------- Funções para Delete ----------------------
    def apagar_um_na_colecao(nome_colecao: str, obj: dict):
        colecao = db.get_collection(nome_colecao)
        colecao.delete_one(obj)
