import pytest
from bot.handler.authentication.auth_manager import AuthManager

@pytest.mark.asyncio
async def test_auth_manager_initialization():
    """Test AuthManager initialization"""
    auth = AuthManager()
    assert auth is not None
    assert auth.phone is None
    assert auth.client is None

@pytest.mark.asyncio
async def test_connection():
    """Test connection to Telegram"""
    auth = AuthManager()
    connected = await auth.connect()
    assert connected is True
    await auth.disconnect() 