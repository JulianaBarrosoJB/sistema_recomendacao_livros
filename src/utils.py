import requests
from PIL import Image
from io import BytesIO
import streamlit as st

## Feito por Juliana Barroso

def carregar_imagem(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        resposta = requests.get(url, headers=headers)
        if resposta.status_code == 200:
            imagem = Image.open(BytesIO(resposta.content))
            return imagem
        else:
            st.warning(f"Não foi possível carregar a imagem")
            return None
    except Exception as e:
        st.warning(f"Erro ao carregar a imagem")
        return None