% rebase('app/views/html/layout.tpl')
<h2>Banco - Livros cadastrados</h2>
<p>Usuário logado: <b>{{usuario}}</b></p>
<form action="/logout" method="post"><button type="submit">Sair</button></form>

% if livros:
<table>
    <tr><th>ID</th><th>Título</th><th>Autor</th><th>Ano</th></tr>
    % for livro in livros:
    <tr>
        <td>{{livro.id}}</td>
        <td>{{livro.titulo}}</td>
        <td>{{livro.autor}}</td>
        <td>{{livro.ano}}</td>
    </tr>
    % end
</table>
% else:
<p>Nenhum livro cadastrado. Use o cURL para cadastrar.</p>
% end
