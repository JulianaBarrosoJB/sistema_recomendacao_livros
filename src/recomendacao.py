import pandas as pd
from sklearn.neighbors import NearestNeighbors

## Feito por Juliana Barroso

def carregar_dados(caminho_books, caminho_ratings):
    books = pd.read_csv(caminho_books, encoding='latin1')
    ratings = pd.read_csv(caminho_ratings, encoding='latin1')
    return books, ratings

def preprocessar_dados(books, ratings, min_avaliacoes_livro=50, min_avaliacoes_usuario=30):
    books.dropna(inplace=True)
    ratings.dropna(inplace=True)

    livros_populares = ratings['ISBN'].value_counts()
    livros_populares = livros_populares[livros_populares >= min_avaliacoes_livro].index
    ratings = ratings[ratings['ISBN'].isin(livros_populares)]

    usuarios_ativos = ratings['User-ID'].value_counts()
    usuarios_ativos = usuarios_ativos[usuarios_ativos >= min_avaliacoes_usuario].index
    ratings = ratings[ratings['User-ID'].isin(usuarios_ativos)]

    df = pd.merge(ratings, books, on='ISBN')
    return df

def criar_matriz_usuario_livro(df):
    user_book_matrix = df.pivot_table(index='User-ID', columns='Book-Title', values='Book-Rating')
    user_book_matrix = user_book_matrix.fillna(0)
    return user_book_matrix

def treinar_modelo_knn(user_book_matrix, n_livros=1000):
    user_book_matrix_reduced = user_book_matrix.iloc[:, :n_livros]
    modelo_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    modelo_knn.fit(user_book_matrix_reduced.T)
    return modelo_knn, user_book_matrix_reduced

def recomendar_livros(titulo, user_book_matrix_reduced, modelo_knn, n_recomendacoes=5):
    if titulo not in user_book_matrix_reduced.columns:
        return None

    livro_index = user_book_matrix_reduced.columns.get_loc(titulo)
    distances, indices = modelo_knn.kneighbors(
        user_book_matrix_reduced.iloc[:, livro_index].values.reshape(1, -1),
        n_neighbors=n_recomendacoes + 1
    )

    recomendacoes = []
    for i in range(1, len(indices.flatten())):
        recomendacoes.append(user_book_matrix_reduced.columns[indices.flatten()[i]])
    return recomendacoes