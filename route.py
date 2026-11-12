from bottle import Bottle, run, request, static_file, redirect

from app.controllers.application import Application

app = Bottle()
ctl = Application()


# ---------------- arquivos estáticos ----------------
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')


# ---------------- páginas ----------------
@app.route('/helper')
def helper():
    return ctl.render('helper')


@app.route('/')
@app.route('/pagina')
def pagina():
    return ctl.render('pagina')


# ---------------- recurso "portal" (login) ----------------
@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')


@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    return ctl.authenticate_user(username, password)


@app.route('/logout', method='POST')
def logout():
    return ctl.logout_user()


# ---------------- recurso "banco" (READ no sistema) ----------------
@app.route('/banco', method='GET')
def banco():
    return ctl.render('banco')


# ---------------- API para o cURL ----------------
@app.route('/api/livros', method='GET')
def api_listar():
    return ctl.api_listar()


@app.route('/api/livros', method='POST')       # CREATE
def api_criar():
    return ctl.api_criar()


@app.route('/api/livros/<id:int>', method='PUT')     # UPDATE
def api_atualizar(id):
    return ctl.api_atualizar(id)


@app.route('/api/livros/<id:int>', method='DELETE')  # DELETE
def api_deletar(id):
    return ctl.api_deletar(id)


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
