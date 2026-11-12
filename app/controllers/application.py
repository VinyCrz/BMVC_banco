import json

from bottle import template, request, response, redirect

from app.controllers.datarecord import DataRecord, LivroRecord


class Application():

    def __init__(self):
        self.pages = {
            'pagina': self.pagina,
            'portal': self.portal,
            'banco': self.banco,
        }
        self.__model = DataRecord()
        self.__livros = LivroRecord()

    # ---------------- páginas (views) ----------------
    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        return content(parameter)

    def get_session_id(self):
        return request.get_cookie('session_id')

    def helper(self):
        return template('app/views/html/helper')

    def pagina(self):
        return template('app/views/html/pagina')

    def portal(self):
        return template('app/views/html/portal', erro=None)

    def banco(self):
        user = self.__model.getCurrentUser(self.get_session_id())
        if not user:
            return redirect('/portal')
        self.__livros.read()
        return template('app/views/html/banco', usuario=user.username,
                        livros=self.__livros.listAll())

    # ---------------- autenticação ----------------
    def authenticate_user(self, username, password):
        session_id = self.__model.checkUser(username, password)
        if session_id:
            response.set_cookie('session_id', session_id, httponly=True,
                                path='/')
            return redirect('/banco')
        return template('app/views/html/portal',
                        erro='Usuário ou senha inválidos')

    def logout_user(self):
        self.__model.logout(self.get_session_id())
        response.delete_cookie('session_id', path='/')
        return redirect('/portal')

    # ---------------- API (CRUD via cURL) ----------------
    def _json(self, data, status=200):
        response.status = status
        response.content_type = 'application/json'
        return json.dumps(data, ensure_ascii=False)

    def _dados(self):
        """Aceita JSON (-H 'Content-Type: application/json') ou form (-d)."""
        if request.json:
            return request.json
        return {k: request.forms.getunicode(k) for k in request.forms.keys()}

    def api_listar(self):
        self.__livros.read()
        return self._json([l.to_dict() for l in self.__livros.listAll()])

    def api_criar(self):
        d = self._dados()
        if not all(d.get(k) for k in ('titulo', 'autor', 'ano')):
            return self._json({'erro': 'informe titulo, autor e ano'}, 400)
        livro = self.__livros.create(d['titulo'], d['autor'], d['ano'])
        return self._json(livro.to_dict(), 201)

    def api_atualizar(self, id):
        d = self._dados()
        livro = self.__livros.update(id, titulo=d.get('titulo'),
                                     autor=d.get('autor'), ano=d.get('ano'))
        if livro is None:
            return self._json({'erro': 'livro não encontrado'}, 404)
        return self._json(livro.to_dict())

    def api_deletar(self, id):
        if not self.__livros.delete(id):
            return self._json({'erro': 'livro não encontrado'}, 404)
        return self._json({'mensagem': f'livro {id} removido'})
