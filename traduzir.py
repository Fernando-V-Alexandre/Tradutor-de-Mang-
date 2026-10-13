import json
import anthropic

client= anthropic.Anthropic()

def traduzir (textos):
    if not textos:
        return []

    prompt = (
        "Você é um tradutor de manga.Traduza as falas abaixo do japonês e ingles para"
        "português brasileiro natural, mantendo o tom e a ordem. As falas são"
        "da mesma página, então use o contexto.Mantenha as traduções curtas,"
        "pois precisam caber em balões.\n\n"
        "Responda APENAS com lista JSON de strings, com exatamente"
        f"{len(textos)} itens, sem explicações e sem markdown\n\n"
        f"{json.dumps(textos, ensure_ascii=False)}"
    )

    resp = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=2000,
        messages=[{"role":"user", "content": prompt}],

    )

    texto = resp.content[0].text.strip()
    texto=texto.replace("```json", "").replace("```","").strip()
    return json.loads(texto)

if __name__=="__main__":
    print(traduzir(["こんにちは", "元気ですか?"]))