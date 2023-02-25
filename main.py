from fastapi import FastAPI
import db.mongo as mongo

app = FastAPI()


@app.get("/")
def hello():
    return {"msg": "hello world"}
