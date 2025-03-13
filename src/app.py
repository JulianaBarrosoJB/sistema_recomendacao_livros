import pandas as pd
import streamlit as st
from recomendacao import carregar_dados, preprocessar_dados, criar_matriz_usuario_livro, treinar_modelo_knn, recomendar_livros
from utils import carregar_imagem
from PIL import Image

## Feito por Juliana Barroso

def main():
    st.title("Sistema de Recomendação de Livros")
    st.write("Digite o título de um livro para receber recomendações.")

    books, ratings = carregar_dados('data/Books.csv', 'data/Ratings.csv')
    df = preprocessar_dados(books, ratings)
    user_book_matrix = criar_matriz_usuario_livro(df)
    modelo_knn, user_book_matrix_reduced = treinar_modelo_knn(user_book_matrix)

    livro_teste = st.text_input("Digite o título do livro:")

    if livro_teste:
        recomendacoes = recomendar_livros(livro_teste, user_book_matrix_reduced, modelo_knn)

        if recomendacoes:
            st.success(f"Recomendações para o livro '{livro_teste}':")
            for livro in recomendacoes:
                st.subheader(livro)
                livro_info = books[books['Book-Title'] == livro].iloc[0]
                url_imagem = livro_info['Image-URL-M']

                if pd.isna(url_imagem) or url_imagem.strip() == "":
                    imagem = Image.open("placeholder.jpg")
                else:
                    imagem = carregar_imagem(url_imagem)

                if imagem:
                    st.image(imagem, caption=livro, width=150)
                else:
                    imagem = Image.open("placeholder.jpg")
                    st.image(imagem, caption=livro, width=150)
        else:
            st.error(f"Livro '{livro_teste}' não encontrado no banco de dados. Tente outro livro")

if __name__ == "__main__":
    main()