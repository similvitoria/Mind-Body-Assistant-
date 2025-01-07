from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from threading import Thread
from support.messeges import send_active_twilio_message
from support.functions.controller import tools
from support.chatbot import chat_with_gpt
from support.functions.python.introduction import introdution
import traceback

app = Flask(__name__)

message_history = []

def handle_messege(phone_number, message):
    try:
        messages = [
            {"role": "system", "content": "Você é um chatbot que auxilia usuários com questões de saúde física e mental."},
            {"role": "user", "content": message}
        ]

        analysis_response = chat_with_gpt(messages, tools)['choices'][0]['message']['content']
        send_active_twilio_message(phone_number, analysis_response)
        #print(f"Análise do problema: {analysis_response}")
            
        message_history.append({"phone_number": phone_number, "message": message, "response": analysis_response})
        
    except Exception as e:
        print(f"Erro: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        for frame in tb:
            print(f"Arquivo: {frame.filename}, Linha: {frame.lineno}, Função: {frame.name}")
        print("Fim do rastreamento.")
        print(message_history)


# Endpoint principal
@app.route('/', methods=['GET', 'POST'])
def webhook():
    try:
        phone_number = request.form.get('From')  
        message = request.form.get('Body')
        
        print(f"Mensagem recebida de {phone_number}: {message}")
        
        thread = Thread(
            target=handle_messege,
            args=(phone_number, message)
        )
        thread.start()
                
        resp = MessagingResponse()
        resp.message('Estou processando sua resposta...')
        return str(resp)
    
    except Exception as e:
        resp = MessagingResponse()
        resp.message('Ocorreu um erro ao processar sua mensagem.')
        return str(resp), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
