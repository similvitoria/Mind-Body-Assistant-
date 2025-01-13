import json
import logging
from typing import Dict, List, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from support.functions.controller import tools
from support.config import ACCOUNT_SID, AUTH_TOKEN
from support.chatbot import chat_with_gpt
from support.functions.python.get_locations import get_nearby_locations_by_city_and_neighborhood

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

user_message_history: Dict[str, List[dict]] = {}

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

def is_audio_message(message):
    """
    Verifica se a mensagem é um áudio.
    """
    return isinstance(message, dict) and 'audio_url' in message

def validate_message(message: str) -> bool:
    """
    Valida se a mensagem é válida para processamento.
    """
    return bool(message and isinstance(message, str) and message.strip())

def handle_location_request(phone_number: str, function_call: dict) -> None:
    """
    Manipula requisições de localização com limite de resultados.
    """
    try:
        # Tenta carregar os argumentos do JSON
        arguments = json.loads(function_call.get('arguments', '{}'))

        query_input = " ".join(str(value) for key, value in arguments.items())
        
        # Chama a função para obter locais próximos
        locations = get_nearby_locations_by_city_and_neighborhood(query_input)
        print(locations)
        
        if locations and isinstance(locations, list):
            # Limita o número de locais para evitar mensagens muito longas
            max_locations = 10
            locations = locations[:max_locations]
            
            locais = "Encontrei os seguintes locais próximos:\n\n" + "\n\n".join(
                f"📍 {local.get('name', 'Nome não disponível')}\n"
                f"📫 Endereço: {local.get('address', 'Endereço não disponível')}"
                for local in locations
            )
            
            if len(locations) == max_locations:
                locais += "\n\nMostrei apenas os 10 locais mais próximos. Se precisar de mais opções, me avise!"
        else:
            locais = "Desculpe, não encontrei locais próximos para o serviço solicitado na região especificada."

        send_active_twilio_message(phone_number, locais)
        logger.info(f"Locais enviados para {phone_number}")

    except json.JSONDecodeError:
        logger.error("Erro ao decodificar argumentos JSON")
        send_active_twilio_message(
            phone_number,
            "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, verifique os dados fornecidos."
        )
    except Exception as e:
        logger.error(f"Erro ao processar pedido de localização: {str(e)}")
        send_active_twilio_message(
            phone_number,
            "Desculpe, ocorreu um erro ao buscar locais. Por favor, tente novamente."
        )
def handle_message(phone_number: str, message: str) -> None:
    """
    Manipula mensagens recebidas com melhor tratamento de erros e validação.
    """
    try:
        if not validate_message(message):
            send_active_twilio_message(
                phone_number, 
                "Desculpe, não consegui entender sua mensagem. Poderia tentar novamente?"
            )
            return

        # Inicializar ou recuperar histórico
        if phone_number not in user_message_history:
            user_message_history[phone_number] = [
                {
                    "role": "system", 
                    "content": "Você é um chatbot que auxilia usuários com questões de saúde física e mental se apresente como tal, coloque emotions(apenas na apresentacao) e seja gentil em poucas palavrar."
                }
            ]

        # Adicionar mensagem do usuário ao histórico
        user_message_history[phone_number].append({
            "role": "user", 
            "content": message.strip()
        })

        

        # Obter resposta do GPT
        response = chat_with_gpt(user_message_history[phone_number], tools)
        
        if not response or 'choices' not in response or not response['choices']:
            raise ValueError("Resposta inválida do chat GPT")

        analysis_response = response['choices'][0]['message'].get('content')
        
        # Processar function calls se existirem
        if 'function_call' in response['choices'][0]['message']:
            function_call = response['choices'][0]['message']['function_call']
            logger.info(f"Função chamada: {function_call['name']}")
            
            if function_call['name'] == 'handle_user_location_request':
                print(function_call)
                handle_location_request(phone_number, function_call)
            
        # Processar resposta normal
        elif analysis_response:
            user_message_history[phone_number].append({
                "role": "assistant", 
                "content": analysis_response
            })
            send_active_twilio_message(phone_number, analysis_response)
            logger.info(f"Resposta enviada para {phone_number}")
        else:
            send_active_twilio_message(
                phone_number, 
                'Por favor, reenvie sua mensagem.'
            )

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}", exc_info=True)
        send_active_twilio_message(
            phone_number,
            "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."
        )