import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in .env file")
        if not (cls.OPENAI_API_KEY.startswith('sk-') or cls.OPENAI_API_KEY.startswith('sk-proj-')):
            raise ValueError("Invalid OpenAI API key format. API key should start with 'sk-' or 'sk-proj-'")
