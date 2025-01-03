from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from threading import Thread
from support.messeges import handle_messege

app = Flask(__name__)

# Histórico em memória
message_history = []

@app.route('/', methods=['GET', 'POST'])
def webhook():
    try:
        phone_number = request.form.get('From')  
        message = request.form.get('Body')
        
        print(f"Mensagem recebida de {phone_number}: {message}")
        
        # Salvar no histórico
        message_history.append({"phone_number": phone_number, "message": message})
        
        # Processar a mensagem em uma thread separada
        thread = Thread(
            target=handle_messege,
            args=(phone_number, message)
        )
        thread.start()
                
        # Resposta ao usuário
        resp = MessagingResponse()
        resp.message('Estou processando sua resposta...')
        return str(resp)
    
    except Exception as e:
        resp = MessagingResponse()
        resp.message('Ocorreu um erro ao processar sua mensagem.')
        return str(resp), 500

if __name__ == "__main__":
    app.run(port=5000)
