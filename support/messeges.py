import json
import logging
from typing import Dict, List
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from support.functions.controller import tools
from support.config import ACCOUNT_SID, AUTH_TOKEN
from support.chatbot import chat_with_gpt
from support.functions.python.get_locations import get_nearby_locations_by_city_and_neighborhood

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

user_message_history: Dict[str, List[dict]] = {}

def split_message(message: str, limit: int = 1500) -> List[str]:
    """
    Divide uma mensagem em partes menores, se necessário, respeitando o limite de caracteres.
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

    return [f"Parte {i+1}/{len(parts)}:\n{part}" for i, part in enumerate(parts)]

def validate_message(message: str) -> bool:
    """
    Valida se a mensagem é válida para processamento.
    """
    return bool(message and isinstance(message, str) and message.strip())

def send_active_twilio_message(to_number: str, message: str) -> bool:
    """
    Envia mensagem via Twilio, dividindo em partes se necessário.
    """
    try:
        if not to_number or not message:
            raise ValueError("Número de telefone e mensagem não podem estar vazios")

        to_number = f'whatsapp:{to_number.lstrip("whatsapp:")}'
        message_parts = split_message(message)
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

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

def handle_location_request(phone_number: str, function_call: dict) -> None:
    """
    Manipula requisições de localização com limite de resultados.
    """

    
    try:
        arguments = json.loads(function_call.get('arguments', '{}'))
        
        if arguments:
            query_input = " ".join(str(value) for value in arguments.values())

            locations = get_nearby_locations_by_city_and_neighborhood(query_input)
            
            if locations and isinstance(locations, list):
                max_locations = 8
                locations = locations[:max_locations]

                locais = "Encontrei os seguintes locais próximos:\n\n" + "\n\n".join(
                    f"📍Nome: {local.get('name', 'Nome não disponível')}\n"
                    f"📫Endereço: {local.get('address', 'Endereço não disponível')}"
                    for local in locations
                )
            else:
                locais = "Desculpe, não encontrei locais próximos para o serviço solicitado na região especificada."
            logger.info(f"Locais encontrados: {locais}")
            send_active_twilio_message(phone_number, locais)
        else:
            send_active_twilio_message(phone_number, "Forneça o atendimento necessário, seu bairro e cidade por favor!")

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
    Processa mensagens de entrada e envia uma resposta adequada ao usuário.
    """
    try:
        if not validate_message(message):
            send_active_twilio_message(
                phone_number,
                "Desculpe, não consegui entender sua mensagem. Poderia tentar novamente?"
            )
            return

        if phone_number not in user_message_history:
            user_message_history[phone_number] = [
                {
                    "role": "system",
                    "content": "Você é um chatbot que auxilia usuários com questões de saúde física e mental. Se apresente como tal, coloque emojis (apenas na apresentação) e seja gentil em poucas palavras."
                }
            ]

        user_message_history[phone_number].append({"role": "user", "content": message.strip()})
        response = chat_with_gpt(user_message_history[phone_number], tools)

        if not response or 'choices' not in response or not response['choices']:
            raise ValueError("Resposta inválida do chat GPT")

        analysis_response = response['choices'][0]['message'].get('content')

        if 'function_call' in response['choices'][0]['message']:
            function_call = response['choices'][0]['message']['function_call']

            if function_call['name'] == 'handle_user_location_request':
                handle_location_request(phone_number, function_call)
            elif analysis_response:
                user_message_history[phone_number].append({"role": "assistant", "content": analysis_response})
                send_active_twilio_message(phone_number, analysis_response)
            else:
                send_active_twilio_message(
                    phone_number,
                    'Por favor, reenvie sua mensagem e informe melhor o problema!'
                )
        elif analysis_response:
            user_message_history[phone_number].append({"role": "assistant", "content": analysis_response})
            send_active_twilio_message(phone_number, analysis_response)
        else:
            send_active_twilio_message(phone_number, 'Por favor, reenvie sua mensagem.')

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}", exc_info=True)
        send_active_twilio_message(
            phone_number,
            "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."
        )
