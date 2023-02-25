import json
import sys

sys.path.insert(1, "/path/to/application/app/folder")
import db.mongo as mongo


class User:
    def __init__(self, dict):

        """Instancia um novo objeto User com os seguintes atributos:

        userdict = {
            "name": 'user1',
            "perfil": 1,
            "username": 'user_name',
            "password": 'user_password'
        }
        """

        for key in dict:
            setattr(self, key, dict[key])
