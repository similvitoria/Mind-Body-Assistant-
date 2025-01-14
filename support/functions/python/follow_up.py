import time
from twilio.base.exceptions import TwilioRestException
import messeges
number: str = "+553171658742"
    
tempo_restante = 3 * 60

while True:
    # Verificar se o tempo acabou
    if tempo_restante <= 0:
        messeges.send_active_twilio_message(number, "Como você está se sentindo?")
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