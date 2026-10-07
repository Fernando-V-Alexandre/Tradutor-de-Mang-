import cv2
from PIL import Image
from manga_ocr import MangaOcr

_mocr = MangaOcr() # carrega o modelo uma vez só

def ler_texto(img, caixa):
    x, y, w, h = caixa
    recorte = img[y:y + h, x:x + w]
    pil=Image.fromarray(cv2.cvtColor(recorte, cv2.COLOR_BAYER_BGR2RGB))
    return _mocr(pil)


if __name__ == "__main__":
    from detectar import detectar_baloes
    img=cv2.imread ("teste.jpg")
    for caixa in detectar_baloes(img):
        print(caixa,"->", ler_texto(img, caixa))
