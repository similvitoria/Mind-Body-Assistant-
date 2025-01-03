import openai
from support.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def chat_with_gpt(user_input):
    
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        content = file.read()    
        
    #print(content)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": user_input}
        ],
        max_tokens=500,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content']

""" conversa = ''
while True:
    conversa += input('usurio: ')
    resp = chat_with_gpt(conversa)
    print(resp)
    conversa += resp """