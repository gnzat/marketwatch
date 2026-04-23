#loads env variables once - central place for secrets
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

REQUIRED_VARS = {
    "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
}

def validate_config():
    missing = [k for k, v in REQUIRED_VARS.items() if not v]
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")