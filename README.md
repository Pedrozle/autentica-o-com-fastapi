# FastAPI

[![Testes](https://github.com/Pedrozle/autentica-o-com-fastapi/actions/workflows/tests.yml/badge.svg?branch=main&event=push)](https://github.com/Pedrozle/autentica-o-com-fastapi/actions/workflows/tests.yml)

## Autenticação com fastapi

Um projeto FastAPI!

### Preparação

Esse projeto tem como objetivo o aprendizado da framework [FastAPI](https://github.com/tiangolo/fastapi) e o intuito de aplicar as práticas de segurança da informação.

Para ajuda ao iniciar projetos em FastAPI, visite a
[documentação online](https://fastapi.tiangolo.com/), que oferece tutoriais, exemplos, guias em desenvolvimento mobile, e uma referência completa na API.

## Instalando

> Para executar este projeto, verifique os requisitos de instalação: `fastapi pymongo  pytest pytest-asyncio python-dotenv`
> se desejar optar por uma instalação limpa, instale e inicie um ambiente de desenvolvimento `venv`, `conda`, etc.

### Instalação

- Requisitos:
  - para que o sistema execute  de forma correta, será necessário criar uma conexão com algum banco de dados, neste projeto foi
utilizado [MongoDB](https://www.mongodb.com/). Será necessário criar uma conta, um projeto e por fim um banco.

  - após isso, é necessário uma conta de email para que seja possível o envio de emails para os usuários no momento do login. [Aqui](https://www.google.com.br/search?q=como+permitir+o+email+para+um+app&sxsrf=AJOqlzVRuN03MfK4U2PKrD_DOGJCQk-wmw%3A1677635427181&source=hp&ei=Y6_-Y_nQCLjK1sQPnMOSqAs&iflsig=AK50M_UAAAAAY_69cztIB-wuqJKYwPgV8QvkaWhDsoWY&ved=0ahUKEwi5jsr9zrn9AhU4pZUCHZyhBLUQ4dUDCAg&uact=5&oq=como+permitir+o+email+para+um+app&gs_lcp=Cgdnd3Mtd2l6EAMyBwghEKABEAoyBwghEKABEAoyBwghEKABEAoyCAghEBYQHhAdMggIIRAWEB4QHTIICCEQFhAeEB0yCAghEBYQHhAdMggIIRAWEB4QHToECCMQJzoECAAQQzoFCC4QgAQ6CwgAEIAEELEDEIMBOhEILhCABBCxAxCDARDHARDRAzoKCC4QxwEQ0QMQQzoICAAQsQMQgwE6CAguEIAEEMkDOggIABCABBCxAzoFCAAQgAQ6BwgAEIAEEAo6BwgAEA0QgAQ6BggAEBYQHjoICAAQFhAeEAo6BQghEKABOgoIIRAWEB4QDxAdOgQIIRAVUABYhVpg6lpoBHAAeACAAesBiAH9LpIBBjAuMzQuMpgBAKABAQ&sclient=gws-wiz) você encontrará a solução para o gmail.

  - por fim, é necessário a criação de um arquivo .env (sem nome, somente a extensão) para guardar os links e senhas de forma segura. Segue o template do arquivo .env:

```js
    DATABASE_CONNECTION= "string de conexao do mongodb"
    EMAIL_ADDRESS = "endereco de email"
    EMAIL_PSW = "senha de acesso de app"
```

executando o código abaixo, você garante que irá instalar todas as dependências necessárias

```py
pip install -r requirements.txt
```

- Faça o clone desse projeto em algum diretório no seu computador
- Abra um terminal neste diretório e execute o comando

```py
uvicorn main:app --reload
```

- Se tudo ocorrer corretamente, o projeto já estará executando no caminho [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

# Documentação

Você encontrará a documentação da API em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Todos as requisições `GET`, `POST`, `PUT` e `DELETE`

# Exemplos
