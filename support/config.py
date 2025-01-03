from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

if not OPENAI_API_KEY or not ACCOUNT_SID or not AUTH_TOKEN:
    raise ValueError("Por favor, configure a OPENAI_API_KEY no arquivo .env")
