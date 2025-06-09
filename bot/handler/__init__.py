"""Initialize command handlers"""
from bot.utils.logging import logger

# Import client
from .client import client

# Import command handlers
try:
    from .start.start import start_handler
    logger.debug("Start command handler loaded")
except ImportError as e:
    logger.error(f"Failed to load start handler: {e}")

try:
    from .help.help import help_handler
    logger.debug("Help command handler loaded")
except ImportError as e:
    logger.error(f"Failed to load help handler: {e}")

try:
    from .settings.settings import settings_handler
    logger.debug("Settings command handler loaded")
except ImportError as e:
    logger.error(f"Failed to load settings handler: {e}")

# Channel Management Handlers
try:
    from .channel_management.add_channel.handler import add_channel_handler
    logger.debug("Add channel handler loaded")
except ImportError as e:
    logger.error(f"Failed to load add channel handler: {e}")

try:
    from .channel_management.list_channels.handler import list_channels_handler
    logger.debug("List channels handler loaded")
except ImportError as e:
    logger.error(f"Failed to load list channels handler: {e}")

try:
    from .channel_management.channel_stats.handler import channel_stats_handler
    logger.debug("Channel stats handler loaded")
except ImportError as e:
    logger.error(f"Failed to load channel stats handler: {e}")

try:
    from .channel_management.member_export.handler import export_members_handler
    logger.debug("Export members handler loaded")
except ImportError as e:
    logger.error(f"Failed to load export members handler: {e}")

# List of all available commands
AVAILABLE_COMMANDS = [
    '/start - شروع کار با ربات',
    '/help - راهنمای دستورات',
    '/settings - تنظیمات ربات',
    '/add_channel - افزودن کانال جدید',
    '/list_channels - مشاهده لیست کانال‌ها',
    '/channel_stats - آمار کانال‌ها',
    '/export_members - دریافت لیست اعضای کانال'
]

logger.info("All command handlers initialized")
