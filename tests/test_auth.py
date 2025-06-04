import unittest
import asyncio
import os
from dotenv import load_dotenv
from bot.handler.authentication.auth_manager import AuthManager

# Load environment variables
load_dotenv()

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.api_id = int(os.getenv('TELEGRAM_API_ID'))
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.auth_manager = AuthManager(self.api_id, self.api_hash)
        
        # Set up event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        """Clean up after tests"""
        # Stop the client
        if self.auth_manager.client and self.auth_manager.client.is_connected():
            self.loop.run_until_complete(self.auth_manager.stop())
        
        # Close the event loop
        self.loop.close()
    
    def test_initialization(self):
        """Test AuthManager initialization"""
        self.assertIsNotNone(self.auth_manager.client)
        self.assertIsNone(self.auth_manager._phone)
        self.assertIsNone(self.auth_manager._code_hash)
    
    async def async_test_connection(self):
        """Test client connection"""
        # Test initial state
        self.assertFalse(self.auth_manager.client.is_connected())
        
        # Test connection
        await self.auth_manager.start()
        self.assertTrue(self.auth_manager.client.is_connected())
        
        # Test disconnection
        await self.auth_manager.stop()
        self.assertFalse(self.auth_manager.client.is_connected())
    
    def test_connection(self):
        """Wrapper for async connection test"""
        self.loop.run_until_complete(self.async_test_connection())
    
    async def async_test_authorization_check(self):
        """Test authorization check"""
        is_authorized = await self.auth_manager.is_authorized()
        # Initially should not be authorized
        self.assertFalse(is_authorized)
        await self.auth_manager.stop()
    
    def test_authorization_check(self):
        """Wrapper for async authorization test"""
        self.loop.run_until_complete(self.async_test_authorization_check())
    
    async def async_test_send_code(self):
        """Test sending verification code"""
        # Test with invalid phone number
        result = await self.auth_manager.send_code("invalid")
        self.assertFalse(result)
        self.assertIsNone(self.auth_manager._code_hash)
        await self.auth_manager.stop()
    
    def test_send_code(self):
        """Wrapper for async send code test"""
        self.loop.run_until_complete(self.async_test_send_code())
    
    async def async_test_sign_in_validation(self):
        """Test sign in validation"""
        # Test sign in without phone and code hash
        success, needs_2fa, error = await self.auth_manager.sign_in("12345")
        self.assertFalse(success)
        self.assertFalse(needs_2fa)
        self.assertTrue(len(error) > 0)
        await self.auth_manager.stop()
    
    def test_sign_in_validation(self):
        """Wrapper for async sign in validation test"""
        self.loop.run_until_complete(self.async_test_sign_in_validation())
    
    def test_cleanup(self):
        """Test state cleanup"""
        # Set some test data
        self.auth_manager._phone = "+1234567890"
        self.auth_manager._code_hash = "test_hash"
        
        # Verify test data is set
        self.assertIsNotNone(self.auth_manager._phone)
        self.assertIsNotNone(self.auth_manager._code_hash)
        
        # Clean up
        self.auth_manager.cleanup()
        
        # Verify cleanup
        self.assertIsNone(self.auth_manager._phone)
        self.assertIsNone(self.auth_manager._code_hash)

if __name__ == '__main__':
    unittest.main() 