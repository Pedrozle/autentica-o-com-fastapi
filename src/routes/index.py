from fastapi import FastAPI, Response, status, Request
from fastapi.responses import HTMLResponse, JSONResponse

from ..services.emailservice import EmailService
from ..services.tokengen import TokenGenerator
from ..models.user import User
from ..db.mongo import Mongo as mongo

app = FastAPI()
emailService = EmailService()
tokengen = TokenGenerator()

# ############################################################# #
#                           ROTAS GET                           #
# ############################################################# #


@app.get("/", response_class=JSONResponse)
async def read_items():
    return {"msg": "aaaaa"}


@app.get("/login", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Droplet</title>
        </head>
        <body>
            <h1>Boas vindas ao <a href="/">Droplet</a>!</h1>
            <form method="post" action="/login" id="login">
                <label for="email">Email</label>
                <input type="email" name="email"/>
                
                <label for="password">Senha</label>
                <input type="password" name="password"/>
                
                <button type="submit" form="login" value="Submit">Login</button>
            </form>
        </body>
    </html>
    """


@app.get("/cadastrar", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Droplet</title>
        </head>
        <body>
            <h1>Boas vindas ao <a href="/">Droplet</a>!</h1>
            <form method="post" action="/cadastrar" id="cadastrar">
                <label for="email">Email</label>
                <input type="email" name="email"/>
                
                <label for="password">Senha</label>
                <input type="password" name="password"/>

                <label for="perfil">Perfil</label>
                <select name="perfil">
                    <option value="1">Usuário</option>
                    <option value="2">Administrador</option>
                </select>
                
                <button type="submit" form="cadastrar" value="Submit">Cadastrar</button>
            </form>
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
                }
                res.status_code = status.HTTP_200_OK

                token = tokengen.gen()
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
