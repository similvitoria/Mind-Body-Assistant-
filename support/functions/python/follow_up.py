import time
from twilio.rest import Client
import logging
from twilio.base.exceptions import TwilioRestException

from dotenv import load_dotenv
import os

load_dotenv()

ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
number: str = "+553171658742"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def split_message(message: str, limit: int = 1500) -> list[str]:
    """
    Divide uma mensagem longa em partes menores respeitando o limite de caracteres.
    """
    if len(message) <= limit:
        return [message]
    
    parts = []
    lines = message.split('\n')
    current_part = ''
    
    for line in lines:
        if len(current_part) + len(line) + 1 <= limit:
            current_part += line + '\n'
        else:
            if current_part:
                parts.append(current_part.strip())
            current_part = line + '\n'
    
    if current_part:
        parts.append(current_part.strip())
    
    # Adiciona numeração às partes se houver mais de uma
    if len(parts) > 1:
        return [f"Parte {i+1}/{len(parts)}:\n{part}" for i, part in enumerate(parts)]
    
    return parts

def send_active_twilio_message(to_number: str, message: str) -> bool:
    """
    Envia mensagem via Twilio, dividindo em partes se necessário.
    """
    try:
        if not to_number or not message:
            raise ValueError("Número de telefone e mensagem não podem estar vazios")

        print(message)
        # Formatação do número WhatsApp
        if to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number[9:]}'
        elif not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'

        # Divide a mensagem em partes se necessário
        message_parts = split_message(message)
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        
        # Envia cada parte da mensagem
        for part in message_parts:
            twilio_message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=part,
                to=to_number
            )
            logger.info(f"Parte da mensagem enviada para {to_number}: {twilio_message.sid}")
        
        return True

    except TwilioRestException as e:
        logger.error(f"Erro Twilio ao enviar mensagem: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar mensagem: {str(e)}")
        return False
    
tempo_restante = 3 * 60

while True:
    # Verificar se o tempo acabou
    if tempo_restante <= 0:
        send_active_twilio_message(number, "Está tudo bem?")
        print("O tempo acabou!")
        break

    # Converter segundos para o formato MM:SS
    minutos = tempo_restante // 60
    segundos = tempo_restante % 60
    print(f"Tempo restante: {minutos:02}:{segundos:02}", end='\r')

    # Aguardar 1 segundo
    time.sleep(1)

    # Reduzir o tempo restante em 1 segundo
    tempo_restante -= 1