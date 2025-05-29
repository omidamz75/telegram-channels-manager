from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

class AuthManager:
    def __init__(self):
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = None
        self.client = None
        
    async def start(self):
        """Initialize and connect client"""
        try:
            self.client = TelegramClient(None, self.api_id, self.api_hash)
            await self.client.connect()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
            
    async def request_code(self, phone_number: str):
        """Request verification code"""
        try:
            await self.start()
            self.phone = phone_number
            return await self.client.send_code_request(phone_number)
        except Exception as e:
            print(f"Code request error: {e}")
            raise

    async def sign_in(self, code: str):
        """Sign in with code"""
        try:
            await self.client.sign_in(phone=self.phone, code=code)
            return True
        except Exception as e:
            print(f"Sign in error: {e}")
            return False
