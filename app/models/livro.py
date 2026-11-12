class Livro():
    """Objeto cadastrado no recurso 'banco' (atributos: titulo, autor, ano)."""

    def __init__(self, id, titulo, autor, ano):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano

    def to_dict(self):
        return {'id': self.id, 'titulo': self.titulo,
                'autor': self.autor, 'ano': self.ano}
