import json
import os
import uuid

from app.models.user_account import UserAccount
from app.models.livro import Livro

DB_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'db')


class DataRecord():
    """Persistência dos usuários (db/user_accounts.json) e controle de sessão."""

    def __init__(self):
        self.__file = os.path.join(DB_DIR, 'user_accounts.json')
        self.__user_accounts = []
        self.__authenticated_users = {}
        self.read()

    def read(self):
        try:
            with open(self.__file, 'r', encoding='utf-8') as f:
                self.__user_accounts = [UserAccount(**d) for d in json.load(f)]
        except FileNotFoundError:
            self.__user_accounts = [UserAccount('admin', '123')]
            self.save()

    def save(self):
        with open(self.__file, 'w', encoding='utf-8') as f:
            json.dump([u.to_dict() for u in self.__user_accounts], f, indent=2)

    def checkUser(self, username, password):
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())
                self.__authenticated_users[session_id] = user
                return session_id
        return None

    def getCurrentUser(self, session_id):
        return self.__authenticated_users.get(session_id)

    def logout(self, session_id):
        self.__authenticated_users.pop(session_id, None)


class LivroRecord():
    """Persistência dos livros (db/livros.json) — usado pelo recurso 'banco'."""

    def __init__(self):
        self.__file = os.path.join(DB_DIR, 'livros.json')
        self.__livros = []
        self.read()

    def read(self):
        try:
            with open(self.__file, 'r', encoding='utf-8') as f:
                self.__livros = [Livro(**d) for d in json.load(f)]
        except FileNotFoundError:
            self.__livros = []
            self.save()

    def save(self):
        with open(self.__file, 'w', encoding='utf-8') as f:
            json.dump([l.to_dict() for l in self.__livros], f,
                      indent=2, ensure_ascii=False)

    def listAll(self):
        return self.__livros

    def get(self, id):
        for livro in self.__livros:
            if livro.id == id:
                return livro
        return None

    def create(self, titulo, autor, ano):
        new_id = max([l.id for l in self.__livros], default=0) + 1
        livro = Livro(new_id, titulo, autor, int(ano))
        self.__livros.append(livro)
        self.save()
        return livro

    def update(self, id, **campos):
        livro = self.get(id)
        if livro is None:
            return None
        for chave in ('titulo', 'autor', 'ano'):
            if chave in campos and campos[chave] is not None:
                valor = int(campos[chave]) if chave == 'ano' else campos[chave]
                setattr(livro, chave, valor)
        self.save()
        return livro

    def delete(self, id):
        livro = self.get(id)
        if livro is None:
            return False
        self.__livros.remove(livro)
        self.save()
        return True
