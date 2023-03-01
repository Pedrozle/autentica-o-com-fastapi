import sys
import time
import threading
from fastapi import FastAPI, Response, status, Request
from fastapi.responses import HTMLResponse, JSONResponse

sys.path.insert(1, "src")

from services.emailservice import EmailService
from services.tokengen import TokenGenerator
from models.user import User
from db.mongo import Mongo as mongo

app = FastAPI()
emailService = EmailService()
tokengen = TokenGenerator()

tokens = {}

# ############################################################# #
#                           ROTAS GET                           #
# ############################################################# #


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>API</title>
        </head>
        <body>
            <h1>FastAPI</h1>
            <p>Se você está vendo esta página então tudo ocorreu corretamente!</p>
            <p>Criado com <a href="https://github.com/tiangolo/fastapi">FastAPI</a> e <a href="https://www.python.org/">Python</a> </p>
            <h2>Documentação</h2>
            <p>Clique <a href="http://localhost:8000/docs">aqui</a> para acessar a documentação!</p>
            <p>Clique <a href="http://localhost:8000/admin/usuarios">aqui</a> para listar todos os usuários!</p>
        </body>
        </html>
    """

# ############################################################# #
#                          ROTAS POST                           #
# ############################################################# #


@app.post("/login", response_class=JSONResponse)
async def logar(req: Request, res: Response):
    result = {"logado": False, "username": "", "perfil": 1}
    user_login = await req.json()
    print(user_login)
    try:
        user: User = mongo.buscar_um_na_colecao(
            "usuarios", {"email": user_login["email"]}
        )
        if user:
            if user["password"] == user_login["password"]:
                print("senhas batem")
                result = {
                    "logado": True,
                    "username": user["username"],
                    "perfil": user["perfil"],
                    "autenticado": False,
                }
                res.status_code = status.HTTP_200_OK

                token = tokengen.gen()
                username = user["username"]
                tokens.update({f"{username}": f"{token}"})
                print(tokens)
                task = threading.Thread(target=async_timer, args=(username,))
                task.start()
                corpo_email = f"""
                    <h1>Tentativa de login</h1>
                    <p>Foi identificado uma tentativa de login para {user['email']}</p>
                    <p>Foi gerado um token de autenticação para você, utilize para validar seu login:</p>
                    <p style="display:block; align: center;">{token}</p>
                """
                await emailService.enviar_email(
                    subj="Autenticação de dois Fatores",
                    corpo_email=corpo_email,
                    email_seg=user["email_seg"],
                )

                return result
            else:
                print("senha incorreta")
                result = {"logado": False, "motivo": "senha incorreta"}
                res.status_code = status.HTTP_401_UNAUTHORIZED
                return result
        else:
            print("usuario não encontrado")
            result = {"logado": False, "motivo": "usuario não encontrado"}
            res.status_code = status.HTTP_404_NOT_FOUND
            return result
    except Exception as e:
        print(f"Error {e}")
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Error": f"{e}"}


@app.post("/login/autenticar", response_class=JSONResponse)
async def autenticar(req: Request, res: Response):
    result = {"logado": False, "username": "", "perfil": 1, "autenticado": False}
    user_data = await req.json()
    try:
        user: User = mongo.buscar_um_na_colecao(
            "usuarios", {"username": user_data["username"]}
        )
        print(user)
        if user:
            username: str = user_data["username"]
            token = user_data["token"]

            if username in tokens:
                if tokens[username] == token:
                    result = {
                        "logado": True,
                        "username": user["username"],
                        "perfil": user["perfil"],
                        "autenticado": True,
                    }
                    res.status_code = status.HTTP_200_OK
                    return result
                else:
                    print("Token incorreto")
                    result = {"logado": False, "motivo": "Token incorreto"}
                    res.status_code = status.HTTP_401_UNAUTHORIZED
                    return result
            else:
                print("Token expirado ou inexistente")
                result = {"logado": False, "motivo": "Token expirado ou inexistente"}
                res.status_code = status.HTTP_401_UNAUTHORIZED
                return result
        else:
            print("usuario não encontrado")
            result = {"logado": False, "motivo": "usuario não encontrado"}
            res.status_code = status.HTTP_404_NOT_FOUND
            return result
    except Exception as e:
        print(f"Error {e}")
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Error": f"{e}"}


@app.post("/cadastrar", response_class=JSONResponse)
async def cadastrar(user: User, res: Response):
    result = {"cadastrado": False}
    try:
        user_saved = mongo.inserir_na_colecao("usuarios", user.__dict__)
        if user_saved:
            res.status_code = status.HTTP_201_CREATED
            result = {"cadastrado": True, "user_id": f"{user_saved.inserted_id}"}
            try:
                subj = "Cadastro Realizado!"
                corpo_email = """
                    <h1>Boas Vindas à Droplet Social</h1>
                    <p>Seu cadastro foi realizado com sucesso</p>
                """
                await emailService.enviar_email(subj, corpo_email, user.email)
            except Exception as er:
                print(f"Error  {er}")
            return result
    except Exception as e:
        print(e)
        result = {"cadastrado": False, "status": "Usuário já cadastrado"}
        res.status_code = status.HTTP_409_CONFLICT
        return result


@app.post("/admin/changepermissions", response_class=JSONResponse)
async def changePermissions(req: Request, res: Response):
    result = {}
    user_data = await req.json()
    username: str = user_data["username"]
    perfil: str = user_data["perfil"]
    try:
        user: User = mongo.buscar_um_na_colecao("usuarios", {"username": username})
        if user:
            result = {"username": username, "perfil antigo": user.perfil}
            user.perfil = perfil
            mongo.atualizar_um_na_colecao(
                "usuarios", {user._id}, {"$set": {"perfil": perfil}}
            )
            print("perfil do usuario atualizado")
            result = {
                "username": username,
                "perfil antigo": user.perfil,
                "perfil atualizado": user.perfil,
                "status": "atualizado",
            }
            res.status_code = status.HTTP_200_OK
            return result
        else:
            print("usuário não encontrado")
            result = {"erro": "username não encontrado"}
            res.status_code = status.HTTP_404_NOT_FOUND
            return result
    except Exception as e:
        print(f"error: {e}")
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        result = {"erro": e}
        return result


# ############################################################# #
#                           ROTAS PUT                           #
# ############################################################# #

# @app.put("/cadastrar", response_class=HTMLResponse)
# async def update():
#     return ''

# ############################################################# #
#                         ROTAS DELETE                          #
# ############################################################# #

# @app.delete("/cadastrar", response_class=HTMLResponse)
# async def delete():
#     return ''


def async_timer(tag):
    time.sleep(300)
    del tokens["{}".format(tag)]
    print(tokens)
