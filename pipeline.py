import cv2
import numpy as np
from PIL import Image

from detectar import detectar_baloes
from ocr import ler_texto
from traduzir import traduzir
from limpar_escrever import apagar_balão, escrever_texo

def traduzir_pagina(caminho_entrada, caminho_saida):
    img = cv2.imread(caminho_entrada)

    # Ordena de cima para baixo (leitura de mangá real seria direita->esquerda,
    # refine isso depois)

    baloes= sorted(detectar_baloes(img), key=lambda b: (b[1], -b[0]))

    originais = [ler_texto(img, b) for b in baloes]
    print("Originais:", originais)

    traduzidos = traduzir(originais)
    print("Traduzidos", traduzidos)

    for b in baloes:
        apagar_balão(img, b)

    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BAYER_BGR2RGB))
    for b, texto in zip(baloes, traduzidos):
        escrever_texo(pil, b, texto)

    pil.save(caminho_saida)

if __name__=="__main__":
    traduzir_pagina("teste.jpg", "resultado.jpg")