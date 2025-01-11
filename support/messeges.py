import json
from support.functions.controller import tools
import traceback
from twilio.rest import Client
from support.config import ACCOUNT_SID, AUTH_TOKEN
from support.chatbot import chat_with_gpt
from support.functions.python.get_locations import get_nearby_locations_by_city_and_neighborhood

user_message_history = {}

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
        
def is_audio_message(message):
    return isinstance(message, dict) and 'audio_url' in message

def handle_message(phone_number, message):
    try:
        if phone_number not in user_message_history:
            user_message_history[phone_number] = [
                {"role": "system", "content": "Você é um chatbot que auxilia usuários com questões de saúde física e mental se apresente como tal, coloque emotions(apenas na apresentacao) e seja gentil em poucas palavrar."}
            ]

        user_message_history[phone_number].append({"role": "user", "content": message})

        response = chat_with_gpt(user_message_history[phone_number], tools)
        
        analysis_response = response['choices'][0]['message']['content']
        
        locais = ''
        user_message_history[phone_number].append({"role": "assistant", "content": analysis_response})
        if 'function_call' in response['choices'][0]['message']:
            print(f"________________________\nFunção Chamada: {response['choices'][0]['message']['function_call']['name']}\n________________________")
            if response['choices'][0]['message']['function_call']['name'] == 'get_location':
                arguments = json.loads(response['choices'][0]['message']['function_call']['arguments'])
                print(arguments, end='\n________________________\n')

                if len(arguments) == 3:
                    # Chamando a função para buscar locais
                    locations = get_nearby_locations_by_city_and_neighborhood(arguments)
                    
                    if locations and isinstance(locations, list):
                        # Formatando a resposta com nome e endereço dos locais encontrados
                        locais = "\n".join(
                            f"- {local.get('name', 'Nome não disponível')}, endereço: {local.get('address', 'Endereço não disponível')}"
                            for local in locations
                        )
                    else:
                        # Caso nenhum local seja encontrado
                        locais = "Desculpe, não encontrei locais próximos para tratar o problema informado na região especificada."
                else:
                    # Caso os argumentos estejam incompletos
                    locais = "Por favor, me informe o problema, a cidade e o bairro para que eu possa ajudá-lo."

                # Enviando mensagem para o usuário
                send_active_twilio_message(phone_number, locais)
                print(f"Resposta enviada para {phone_number}: {locais}")
                
        elif analysis_response:
            send_active_twilio_message(phone_number, analysis_response)
            print(f"Resposta enviada para {phone_number}: {analysis_response}")
        else:
            send_active_twilio_message(phone_number, 'Por favor reenvie a mensagem!') 
            print(f"Resposta enviada para {phone_number}: Por favor reenvie a mensagem!")
            
        print('----------------------------------------------------')
    
    except Exception as e:
        print(f"\n------------------------------------------\nErro: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        for frame in tb:
            print(f"Arquivo: {frame.filename}, Linha: {frame.lineno}, Função: {frame.name}")
        print("Fim do rastreamento.\n-------------------------------------------------\n")
        print(user_message_history.get(phone_number, []), end='\n\n')