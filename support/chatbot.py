import openai
from support.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def chat_with_gpt(messages: dict, tools):
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",  # Modelo com suporte para function calling
        messages=messages,
        max_tokens=500,
        temperature=0.7,
        functions=tools,  
        function_call="auto"  # Permite que o modelo sugira chamadas de função
    )
    return response

""" def transcribe_audio(audio_url):
    try:
        # Abrindo o arquivo de áudio
        with open(audio_url, "rb") as audio_file:
            # Enviando o áudio para a transcrição
            response = openai.Audio.transcribe(model="whisper-1", file=audio_file)
        
            return response['text']
    
    except Exception as e:
        print(f"Erro ao transcrever o áudio: {e}")
        return None """