% rebase('app/views/html/layout.tpl')
<h2>Portal - Login</h2>
% if erro:
    <p class="erro">{{erro}}</p>
% end
<form action="/portal" method="post">
    <label>Usuário: <input type="text" name="username" required></label><br>
    <label>Senha: <input type="password" name="password" required></label><br>
    <button type="submit">Entrar</button>
</form>
