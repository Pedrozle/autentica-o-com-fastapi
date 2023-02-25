from fastapi import FastAPI

# import db.mongo as mongo
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Droplet</title>
        </head>
        <body>
            <h1>Boas vindas ao <a href="/">Droplet</a>!</h1>
            <p>Faça login ou cadastre-se para acessar a página</p>
            <a href="/login">Login</a>
            <a href="/cadastrar">Cadastrar</a>
        </body>
    </html>
    """


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


@app.post("/login", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Droplet</title>
        </head>
        <body>
            <h1>Boas vindas ao <a href="/">Droplet</a>!</h1>
            <p>Usuário Logado</p>
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


@app.post("/cadastrar", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Droplet</title>
        </head>
        <body>
            <h1>Boas vindas ao <a href="/">Droplet</a>!</h1>
            <p>Usuário Cadastrador</p>
        </body>
    </html>
    """
