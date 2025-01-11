from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from threading import Thread
from support.messeges import handle_message
from support.chatbot import chat_with_gpt

app = Flask(__name__)

""" user_message_history = {}

def handle_messege(phone_number, message):
    try:
        if phone_number not in user_message_history:
            user_message_history[phone_number] = [
                {"role": "system", "content": "Você é um chatbot que auxilia usuários com questões de saúde física e mental."}
            ]
        
        user_message_history[phone_number].append({"role": "user", "content": message})

        response = chat_with_gpt(user_message_history[phone_number], tools)
        
        analysis_response = response['choices'][0]['message']['content']

        user_message_history[phone_number].append({"role": "assistant", "content": analysis_response})

        send_active_twilio_message(phone_number, analysis_response)
        
        print(f"Resposta enviada para {phone_number}: {analysis_response}")
        print(f"Função chamada {response['choices'][0]['message']['function_call']['name']}")
    
    except Exception as e:
        print(f"Erro: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        for frame in tb:
            print(f"Arquivo: {frame.filename}, Linha: {frame.lineno}, Função: {frame.name}")
        print("Fim do rastreamento.")
        print(user_message_history.get(phone_number, [])) """


# Endpoint principal
@app.route('/', methods=['GET', 'POST'])
def webhook():
    try:
        phone_number = request.form.get('From')  
        message = request.form.get('Body')
        
        print(f"Mensagem recebida de {phone_number}: {message}")
        
        thread = Thread(
            target=handle_message,
            args=(phone_number, message)
        )
        thread.start()
                
        resp = MessagingResponse()
    
        return str(resp)
    
    except Exception as e:
        resp = MessagingResponse()
        resp.message('Ocorreu um erro ao processar sua mensagem.')
        return str(resp), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
