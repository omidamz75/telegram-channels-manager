PS C:\Users\KPC\Desktop\telegram-manager> pytest -v -s
============================================= test session starts =============================================
platform win32 -- Python 3.12.6, pytest-7.4.3, pluggy-1.6.0 -- C:\Users\KPC\Desktop\telegram-manager\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\KPC\Desktop\telegram-manager
plugins: anyio-4.9.0, asyncio-0.21.1, mock-3.12.0
asyncio: mode=Mode.STRICT
collected 3 items

tests/test_help.py::test_help_command FAILED
tests/test_settings.py::test_settings_command FAILED
tests/test_settings.py::test_settings_callback FAILED

================================================== FAILURES =================================================== 
______________________________________________ test_help_command ______________________________________________ 

    @pytest.mark.asyncio
    async def test_help_command():
        # Mock objects
>       update = Update.de_json({
            "message": {
                "message_id": 1,
                "text": "/help",
                "chat": {"id": 123, "type": "private"}
            }
        }, None)

tests\test_help.py:9:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
venv\Lib\site-packages\telegram\_update.py:424: in de_json
    data["message"] = Message.de_json(data.get("message"), bot)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'telegram._message.Message'>
data = {'chat': {'id': 123, 'type': 'private'}, 'from_user': None, 'message_id': 1, 'sender_chat': None, ...}   
bot = None

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["Message"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        # Get the local timezone from the bot if it has defaults
        loc_tzinfo = extract_tzinfo_from_defaults(bot)

        data["from_user"] = User.de_json(data.pop("from", None), bot)
        data["sender_chat"] = Chat.de_json(data.get("sender_chat"), bot)
>       data["date"] = from_timestamp(data["date"], tzinfo=loc_tzinfo)
E       KeyError: 'date'

venv\Lib\site-packages\telegram\_message.py:900: KeyError
____________________________________________ test_settings_command ____________________________________________ 

    @pytest.mark.asyncio
    async def test_settings_command():
>       update = Update.de_json({
            "message": {
                "message_id": 1,
                "text": "/settings",
                "chat": {"id": 123, "type": "private"}
            }
        }, None)

tests\test_settings.py:8:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
venv\Lib\site-packages\telegram\_update.py:424: in de_json
    data["message"] = Message.de_json(data.get("message"), bot)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'telegram._message.Message'>
data = {'chat': {'id': 123, 'type': 'private'}, 'from_user': None, 'message_id': 1, 'sender_chat': None, ...}   
bot = None

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["Message"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None
    
        # Get the local timezone from the bot if it has defaults
        loc_tzinfo = extract_tzinfo_from_defaults(bot)

        data["from_user"] = User.de_json(data.pop("from", None), bot)
        data["sender_chat"] = Chat.de_json(data.get("sender_chat"), bot)
>       data["date"] = from_timestamp(data["date"], tzinfo=loc_tzinfo)
E       KeyError: 'date'

venv\Lib\site-packages\telegram\_message.py:900: KeyError
___________________________________________ test_settings_callback ____________________________________________ 

    @pytest.mark.asyncio
    async def test_settings_callback():
        query = CallbackQuery(id='123', from_user=None, chat_instance='123', data='setting_timing')
        update = Update(0, callback_query=query)

>       context = ContextTypes.DEFAULT_TYPE()

tests\test_settings.py:28: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = telegram.ext._callbackcontext.CallbackContext[telegram.ext._extbot.ExtBot[None], typing.Dict[typing.Any, 
typing.Any], typing.Dict[typing.Any, typing.Any], typing.Dict[typing.Any, typing.Any]]
args = (), kwargs = {}

    def __call__(self, *args, **kwargs):
        if not self._inst:
>       result = self.__origin__(*args, **kwargs)
E       TypeError: CallbackContext.__init__() missing 1 required positional argument: 'application'

C:\Python312\Lib\typing.py:1184: TypeError
=========================================== short test summary info =========================================== 
FAILED tests/test_help.py::test_help_command - KeyError: 'date'
FAILED tests/test_settings.py::test_settings_command - KeyError: 'date'
FAILED tests/test_settings.py::test_settings_callback - TypeError: CallbackContext.__init__() missing 1 required positional argument: 'application'
============================================== 3 failed in 1.03s ============================================== 