import cv2

def detectar_baloes(img):
    # cv2.imread retorna uma imagem colorida BGR, não dados Bayer crus.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w =gray.shape

    # Pixels bem claros viram branco, o resto preto

    _, mask=cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    baloes= []
    for c in contornos:
        x, y, bw, bh =cv2.boundingRect(c)
        area= bw * bh

        # Ignora regiões pequenas demais ou enormes (margem da página)

        if area <3000 or area >0.5 * w * h:
            continue
# Um balão tem texto: proporção de pixels escuros dentro dele

        roi= gray[y:y + bh, x:x + bw]
        escuros= (roi <100).mean()
        if 0.02< escuros <0.35:
            baloes.append((x, y, bw, bh))
    return baloes


if __name__ == "__main__":
    img=cv2.imread("teste.jpg")
    baloes=detectar_baloes(img)
    print(f"{len(baloes)} balões encontrados")

    for (x, y, w, h) in baloes:
        cv2.rectangle(img, (x,y), (x + w, y + h), (0, 0, 255), 3)
    cv2.imwrite("debug_baloes.jpg", img)


