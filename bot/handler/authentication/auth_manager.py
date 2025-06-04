from telethon import TelegramClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AuthManager:
    def __init__(self):
        """Initialize AuthManager with API credentials"""
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = None
        self.client = None

    async def connect(self) -> bool:
        """Create and connect the Telethon client"""
        try:
            self.client = TelegramClient('user_session', self.api_id, self.api_hash)
            await self.client.connect()
            return True
        except Exception as e:
            print(f"Error connecting to Telegram: {e}")
            return False

    async def request_verification_code(self, phone_number: str) -> bool:
        """Request verification code for the given phone number"""
        try:
            if not self.client:
                await self.connect()
            
            self.phone = phone_number
            await self.client.send_code_request(phone_number)
            return True
        except Exception as e:
            print(f"Error requesting verification code: {e}")
            return False

    async def sign_in_with_code(self, code: str) -> bool:
        """Sign in with the received verification code"""
        try:
            if not self.phone:
                return False
                
            await self.client.sign_in(phone=self.phone, code=code)
            return True
        except Exception as e:
            print(f"Error signing in: {e}")
            return False

    async def disconnect(self):
        """Disconnect the client"""
        if self.client:
            await self.client.disconnect() 