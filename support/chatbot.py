import openai
from support.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def chat_with_gpt(messages: dict, tools):
    
    """ with open('prompt.txt', 'r', encoding='utf-8') as file:
        content = file.read()     """
        
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",  # Modelo com suporte para function calling
        messages=messages,
        max_tokens=500,
        temperature=0.7,
        functions=tools,  # Inclui as funções no request
        function_call="auto"  # Permite que o modelo sugira chamadas de função
    )
    
    return response

""" conversa = ''
while True:
    conversa += input('usurio: ')
    resp = chat_with_gpt(conversa)
    print(resp)
    conversa += resp """