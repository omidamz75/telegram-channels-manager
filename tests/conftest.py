import pytest
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure pytest
def pytest_configure(config):
    """Configure pytest"""
    # Register async marker
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close() 