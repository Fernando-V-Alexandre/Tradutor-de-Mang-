import os
import uuid
from flask import Flask, request, send_file, render_template_string
from pipeline import traduzir_pagina

app=Flask(__name__)
os.makedirs("uploads", exist_ok=True)

HTML = """
<h1>Tradutor de Mangá</h1>
<form method="post" enctype="multipart/form-data">
    <input type="file" name"pagina" accept="image/*" required>x
    <button type="submit">Traduzir</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def index ():
    if request.method=="POST":
        arquivo = request.files["pagina"]
        nome=uuid.uuid4().hex
        entrada=f"uploads/{nome}_in.jpg"
        saida=f"uploads/{nome}_out.jpg"
        arquivo.save(entrada)
        traduzir_pagina(entrada,saida)
        return send_file(saida, mimetype="image/jpeg")
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)