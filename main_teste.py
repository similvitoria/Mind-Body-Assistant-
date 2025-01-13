import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from threading import Thread
from support.messeges import handle_message

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    """
    Endpoint principal para receber mensagens do Twilio.
    """
    try:
        phone_number = request.form.get('From')
        message = request.form.get('Body')
        
        if not phone_number or not message:
            logger.warning("Requisição recebida sem número de telefone ou mensagem")
            return str(MessagingResponse()), 400
            
        logger.info(f"Mensagem recebida de {phone_number}: {message}")
        
        # Processa a mensagem em uma thread separada
        Thread(
            target=handle_message,
            args=(phone_number, message),
            daemon=True  # Permite que o servidor seja encerrado mesmo com threads em execução
        ).start()
                
        return str(MessagingResponse())
    
    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}", exc_info=True)
        resp = MessagingResponse()
        resp.message('Ocorreu um erro ao processar sua mensagem.')
        return str(resp), 500

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',  # Permite acesso externo
        port=5000,
        debug=True
    )