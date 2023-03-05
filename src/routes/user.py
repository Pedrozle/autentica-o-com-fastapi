import sys
import time
import threading
from fastapi import FastAPI, Response, status, Request
from fastapi.responses import HTMLResponse, JSONResponse

from src.services.emailservice import EmailService
from src.services.tokengen import TokenGenerator
from src.services.hashgen import HashGenerator
from src.models.user import User, Login, Autenticatable, UpdateLogin
from src.db.mongo import Mongo as mongo

app = FastAPI()
emailService = EmailService()
tokengen = TokenGenerator()
hashgen = HashGenerator()

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
            <h1><a href="http://localhost:8000/">FastAPI</a></h1>
            <p>Se você está vendo esta página então tudo ocorreu corretamente!</p>
            <p>Criado com <a href="https://github.com/tiangolo/fastapi">FastAPI</a> e <a href="https://www.python.org/">Python</a> </p>
            <h2>Documentação</h2>
            <p>Clique <a href="http://localhost:8000/docs">aqui</a> para acessar a documentação!</p>
            <p>Clique <a href="http://localhost:8000/admin/usuarios">aqui</a> para listar todos os usuários!</p>
        </body>
        </html>
    """


@app.get("/admin/usuarios", response_class=HTMLResponse)
async def getUsuarios():
    usuarios = mongo.buscar_varios_na_colecao("usuarios")
    code = ""
    for i, usuario in enumerate(usuarios):
        username = usuario["username"]
        nome = usuario["name"]
        email = usuario["email"]
        email_seg = usuario["email_seg"]
        perfil = usuario["perfil"]
        json = "{"
        json += f'"usuario" : {username},"nome" : {nome},"email" : {email},"email_seg" : {email_seg},"perfil" : {"Administrador" if perfil == 1 else "Usuario"}'
        json += "}"
        code += f"<code class='prettyprint'>{json}</code><br>"
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>API</title>
        </head>
        <body>
            <h1><a href="http://localhost:8000/">FastAPI</a></h1>
            <p>Se você está vendo esta página então tudo ocorreu corretamente!</p>
            <p>Criado com <a href="https://github.com/tiangolo/fastapi">FastAPI</a> e <a href="https://www.python.org/">Python</a> </p>
            <h2>Admin, listagem de usuarios</h2>
            {code}
            <script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js"></script>
        </body>
        </html>
    """


# ############################################################# #
#                          ROTAS POST                           #
# ############################################################# #


@app.post("/login", response_class=JSONResponse)
async def logar(user_login: Login, res: Response):
    result = {"logado": False, "username": "", "perfil": 1}
    user_email = user_login.__dict__["email"]
    user_pwd = user_login.__dict__["password"]
    try:
        user = mongo.buscar_um_na_colecao("usuarios", {"email": user_email})
        if user:
            if hashgen.verify(user["password"], user_pwd):
                print("senhas batem")
                result = {
                    "logado": True,
                    "username": user["username"],
                    "perfil": user["perfil"],
                    "autenticado": False,
                }
                res.status_code = status.HTTP_200_OK

                username = user["username"]
                token_string = "Um token já foi enviado anteriormente, utilize-o"
                if username not in tokens:
                    token = tokengen.gen()
                    token_string = ""
                    tokens.update({f"{username}": f"{token}"})
                    print(tokens)
                    task = threading.Thread(target=async_timer, args=(username,))
                    task.start()
                corpo_email = f"""
                    <h1>Tentativa de login</h1>
                    <p>Foi identificado uma tentativa de login para {user['email']}</p>
                    <p>Foi gerado um token de autenticação para você, utilize para validar seu login:</p>
                    <p style="display:block; align: center;">{token if token_string == '' else token_string}</p>
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
async def autenticar(user_data: Autenticatable, res: Response):
    result = {"logado": False, "username": "", "perfil": 1, "autenticado": False}
    try:
        user: User = mongo.buscar_um_na_colecao(
            "usuarios", {"username": user_data.__dict__["username"]}
        )
        print(user)
        if user:
            username: str = user_data.__dict__["username"]
            token = user_data.__dict__["token"]

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

    pwd = user.__dict__["password"]
    pwd_hash = hashgen.gen(pwd)
    user.__dict__["password"] = pwd_hash
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
async def changePermissions(user_data: UpdateLogin, res: Response):
    result = {}
    username: str = user_data.__dict__["username"]
    perfil: str = user_data.__dict__["perfil"]
    try:
        user: User = mongo.buscar_um_na_colecao("usuarios", {"username": username})
        if user:
            result = {"username": username, "perfil_antigo": user["perfil"]}
            user["perfil"] = perfil

            filter = {"_id": user["_id"]}
            new_values = {"$set": {"perfil": perfil}}

            mongo.atualizar_um_na_colecao("usuarios", filter, new_values)
            print("perfil do usuario atualizado")
            result["perfil_atualizado"] = user["perfil"]
            result["status"] = "atualizado"
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
