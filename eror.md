=================================== 1 failed, 1 passed, 1 warning in 0.73s ==================================== 
PS C:\Users\KPC\Desktop\telegram-manager> pytest tests/test_add_channel.py -v
============================================= test session starts =============================================
platform win32 -- Python 3.12.6, pytest-7.4.3, pluggy-1.6.0 -- C:\Users\KPC\Desktop\telegram-manager\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\KPC\Desktop\telegram-manager
plugins: anyio-4.9.0, asyncio-0.21.1, mock-3.12.0
asyncio: mode=Mode.STRICT
collected 2 items

tests/test_add_channel.py::test_start_add_channel PASSED                                                 [ 50%] 

============================================== warnings summary =============================================== 
bot\handler\channel_management\add_channel\handler.py:68
  C:\Users\KPC\Desktop\telegram-manager\bot\handler\channel_management\add_channel\handler.py:68: PTBUserWarning: If 'per_message=False', 'CallbackQueryHandler' will not be tracked for every message. Read this FAQ entry to learn more about the per_* settings: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-Asked-Questions#what-do-the-per_-settings-in-conversationhandler-do.
    add_channel_handler = ConversationHandler(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================== 2 passed, 1 warning in 0.50s ========================================= 