import openai

chaveAPI = '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'
openai.api_key = chaveAPI

def enviar_mensagem(msg):
    response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "user", "content": msg}
    ],)

    return response["choices"][0]["message"]

print(enviar_mensagem("Quando finalizou a segunda guerra mundial?"))
