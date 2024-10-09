import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60)
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv(
    "JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7
)
PSQL_CONNECTION_STRING = os.getenv("DATABASE_URL", "").replace(
    "postgres", "postgresql+asyncpg"
)
REDIS_URL = os.getenv("REDIS_URL")
CORS_ORIGINS = [url.strip() for url in os.getenv("CORS_ORIGINS", "").split(",")]
FB_CLIENT_ID = os.getenv("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.getenv("FB_CLIENT_SECRET")
FB_REDIRECT = os.getenv("FB_REDIRECT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0"))
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET_KEY = os.getenv("PAYPAL_SECRET_KEY")
PAYPAL_API_URL = os.getenv("PAYPAL_API_URL", "https://api-m.sandbox.paypal.com")
PAYPAL_WEBHOOK_ID = os.getenv("PAYPAL_WEBHOOK_ID")
DEMO_PHONE_NUMBERS = [
    phone.strip() for phone in os.getenv("DEMO_PHONE_NUMBERS", "").split(",")
]
DEMO_TOPIC = os.getenv("DEMO_TOPIC", "economy")
TIMEZONE = os.getenv("TIMEZONE", "America/Los_Angeles")
