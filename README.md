# BMVC - Banco de Livros

Sistema web feito com o framework BMVC (Bottle + arquitetura MVC). Ele oferece dois recursos: **portal** e **banco**.

- **portal** (`/portal`): tela de login. Os usuários seguem o modelo `UserAccount` e ficam em `db/user_accounts.json`. Usuário padrão: `admin`, senha `123`.
- **banco** (`/banco`): só pode ser acessado por usuários autenticados (cookie de sessão). Mostra a lista de livros cadastrados. Este é o **READ** feito pelo próprio sistema.

Tema: **livros**. Cada livro tem os atributos `id`, `titulo`, `autor` e `ano`.

## Arquitetura

```
route.py                        -> rotas (Bottle)
app/controllers/application.py  -> controlador (renderiza páginas, login, API)
app/controllers/datarecord.py   -> persistência JSON (usuários/sessões e livros)
app/models/user_account.py      -> modelo UserAccount
app/models/livro.py             -> modelo Livro
app/views/html/*.tpl            -> views (layout, pagina, portal, banco, helper)
app/static/css/style.css        -> estilo
db/*.json                       -> "banco de dados"
```

## Como executar

```bash
pip install bottle
python3 route.py
```

Acesse http://localhost:8080/portal e entre com `admin` / `123`. Você será levado ao `/banco`.

## CRUD via cURL (terminal Linux)

Requisito mínimo: CREATE e DELETE. O UPDATE também foi implementado.

```bash
# CREATE: cadastrar um livro
curl -X POST http://localhost:8080/api/livros \
     -H "Content-Type: application/json" \
     -d '{"titulo":"Dom Casmurro","autor":"Machado de Assis","ano":1899}'

# CREATE: versão com formulário
curl -X POST http://localhost:8080/api/livros -d "titulo=O Cortiço&autor=Aluísio Azevedo&ano=1890"

# UPDATE: alterar o livro de id 2
curl -X PUT http://localhost:8080/api/livros/2 \
     -H "Content-Type: application/json" -d '{"ano":1891}'

# DELETE: remover o livro de id 2
curl -X DELETE http://localhost:8080/api/livros/2

# (opcional) listar em JSON
curl http://localhost:8080/api/livros
```

Depois de cada comando, recarregue `/banco` no navegador para ver a lista atualizada.
