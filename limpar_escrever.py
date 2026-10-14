import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTE= "fonte.ttf"

def apagar_balão(img, caixa, margem=8):
    x, y, w, h = caixa
    cv2.rectangle(img,
                    (x + margem, y + margem),
                    (x + w - margem, y + h - margem),
                    (255, 255, 255),-1)


def quebrar_linhas(draw, texto, fonte, largura_max):
    palavras=texto.split()
    linhas,atual =[],""
    for p in palavras:
        teste=f"{atual} {p}".strip()
        if draw.textlength(teste, font=fonte) <=largura_max:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
                atual = p
    if atual:
        linhas.append(atual)
    return linhas

def escrever_texo(pil_img, caixa, texto, margem=12):
    draw = ImageDraw.Draw(pil_img)
    x ,y, w, h = caixa
    largura = w - 2 * margem
    altura = h - 2 * margem

    for tamanho in range(40, 8, -1):
        fonte = ImageFont.truetype (FONTE, tamanho)
        linhas= quebrar_linhas(draw, texto, fonte, largura)
        altura_linha = tamanho * 1.15
        if len (linhas) * altura_linha <= altura:
            break

    # Centraliza o bloco de texto dentro do balão
    y_atual= y + margem + (altura - len(linhas) * altura_linha) / 2
    for linha in linhas:
        larg_linha = draw.textlength(linha, font=fonte)
        x_linha= x + (w - larg_linha) / 2
        draw.text((x_linha, y_atual), linha, font=fonte, fill = (0, 0, 0))
        y_atual += altura_linha 