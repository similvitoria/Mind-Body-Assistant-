from twilio.rest import Client
from support.config import ACCOUNT_SID, AUTH_TOKEN
from support.chatbot import chat_with_gpt

def send_active_twilio_message(to_number: str, message: str):
    try:
        print(message)
        if to_number.startswith('whatsapp:'):
            to_number = to_number[9:]
            to_number = f'whatsapp:{to_number}'

        message = Client(ACCOUNT_SID, AUTH_TOKEN).messages.create(
            from_=f'whatsapp:+14155238886',
            body=message,
            to=to_number
        )
        print(f"Active message sent to {to_number}: {message.sid}")
    except Exception as e:
        print(f"Error sending active message: {e}")
        
def handle_messege(phone_number: str, user_messege: str):
    try:
        resp = chat_with_gpt(user_messege)
        print(f'Resposta do chatbot: {resp}')
        send_active_twilio_message(phone_number, resp)
    except Exception as e:
        print(f"Erro ao processar mensagem de {phone_number}: {e}")
