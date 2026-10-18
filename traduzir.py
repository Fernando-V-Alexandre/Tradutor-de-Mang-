import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY não encontrada. Adicione GEMINI_API_KEY=sua_chave ao arquivo .env"
    )

client = genai.Client(api_key=api_key)

TAMANHO_LOTE = 20


def _traduzir_lote(textos):

    prompt = (
        "Você é um tradutor de manga.Traduza as falas abaixo do japonês e ingles para"
        "português brasileiro natural, mantendo o tom e a ordem. As falas são"
        "da mesma página, então use o contexto.Mantenha as traduções curtas,"
        "pois precisam caber em balões.\n\n"
        "Responda APENAS com lista JSON de strings, com exatamente"
        f"{len(textos)} itens, sem explicações e sem markdown\n\n"
        f"{json.dumps(textos, ensure_ascii=False)}"
    )

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=8192,
            response_mime_type="application/json",
            response_schema=types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                min_items=len(textos),
                max_items=len(textos),
            ),
        ),
    )

    try:
        traducoes = resp.parsed if resp.parsed is not None else json.loads(resp.text)
    except json.JSONDecodeError as erro:
        raise RuntimeError(
            "O Gemini retornou uma resposta incompleta. Tente traduzir a imagem novamente."
        ) from erro

    if not isinstance(traducoes, list) or len(traducoes) != len(textos):
        raise RuntimeError("O Gemini não retornou todas as traduções esperadas. Tente novamente.")

    return [str(traducao) for traducao in traducoes]


def traduzir(textos):
    if not textos:
        return []

    traducoes = []
    for inicio in range(0, len(textos), TAMANHO_LOTE):
        traducoes.extend(_traduzir_lote(textos[inicio:inicio + TAMANHO_LOTE]))
    return traducoes

if __name__=="__main__":
    print(traduzir(["こんにちは", "元気ですか?"]))
