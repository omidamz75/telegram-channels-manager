"""Channel validation functionality for member extraction."""

from typing import Optional, Tuple, Union
from telethon.tl.types import Channel, Chat, User, PeerChannel
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    UsernameInvalidError,
    UsernameNotOccupiedError,
    BotMethodInvalidError,
    ChatAdminRequiredError,
    UserNotParticipantError
)
from bot.utils.logging import logger

class ChannelValidator:
    """Validates and retrieves information about Telegram channels."""

    def __init__(self, client):
        """Initialize the validator with a Telethon client.
        
        Args:
            client: An authenticated Telethon client instance
        """
        self.client = client

    async def validate_channel(self, channel_id: str) -> Tuple[bool, str, Optional[Channel]]:
        """Validate a channel and return its information.
        
        Args:
            channel_id: Channel username, invite link, or numeric ID
            
        Returns:
            Tuple containing:
            - Boolean indicating if channel is valid
            - Error message if invalid, empty string if valid
            - Channel object if valid, None if invalid
        """
        try:
            # Clean up the channel ID
            clean_id = self._clean_channel_id(channel_id)
            logger.debug(f"Cleaned channel ID: {clean_id}")
            
            # Check if it's a private invite link
            if clean_id.startswith('+'):
                help_message = (
                    "⚠️ به دلیل محدودیت‌های تلگرام، ربات نمی‌تواند از لینک دعوت استفاده کند.\n\n"
                    "لطفاً به یکی از این روش‌ها عمل کنید:\n\n"
                    "1️⃣ ربات را به کانال اضافه کرده و ادمین کنید\n"
                    "2️⃣ سپس یکی از این موارد را ارسال کنید:\n"
                    "   • نام کاربری کانال (مثال: @channelname)\n"
                    "   • آیدی عددی کانال (مثال: -1001234567890)\n\n"
                    "📌 برای پیدا کردن آیدی عددی کانال:\n"
                    "• یک پیام از کانال را به @getidsbot فوروارد کنید\n"
                    "• یا در نسخه وب تلگرام، روی پیامی از کانال کلیک راست کرده و 'Copy Post Link' را انتخاب کنید"
                )
                return False, help_message, None

            # Try to get entity
            try:
                # First try as numeric ID
                if clean_id.startswith('-100'):
                    try:
                        channel_id = int(clean_id[4:])  # Remove -100 prefix
                        entity = await self.client.get_entity(PeerChannel(channel_id))
                    except ValueError:
                        # If conversion fails, try as regular username/identifier
                        entity = await self.client.get_entity(clean_id)
                else:
                    # Try as regular username/identifier
                    entity = await self.client.get_entity(clean_id)
                
                logger.debug(f"Got entity type: {type(entity).__name__}")
                
                # Check if it's actually a channel/supergroup
                if not isinstance(entity, (Channel, Chat)):
                    return False, "این شناسه متعلق به یک کانال یا گروه نیست. لطفاً شناسه معتبر وارد کنید.", None
                
                # Get full channel info and check permissions
                full_channel = await self.client(GetFullChannelRequest(entity))
                me = await self.client.get_me()
                permissions = await self.client.get_permissions(entity, me)
                has_admin_rights = getattr(permissions, 'is_admin', False)
                
                if not has_admin_rights:
                    return False, "ربات باید ادمین کانال باشد. لطفاً ابتدا ربات را ادمین کانال کنید.", None
                
                return True, "", entity

            except ValueError:
                return False, "فرمت آیدی نامعتبر است. لطفاً یک نام کاربری یا آیدی عددی معتبر وارد کنید.", None
                
        except ChannelInvalidError:
            return False, "این کانال وجود ندارد یا نامعتبر است.", None
        except ChannelPrivateError:
            return False, "این کانال خصوصی است یا ربات به آن دسترسی ندارد. لطفاً ابتدا ربات را به کانال اضافه کنید.", None
        except (UsernameInvalidError, UsernameNotOccupiedError):
            return False, "این نام کاربری نامعتبر است یا وجود ندارد.", None
        except ChatAdminRequiredError:
            return False, "برای انجام این عملیات، ربات باید ادمین کانال باشد.", None
        except UserNotParticipantError:
            return False, "ربات عضو کانال نیست. لطفاً ابتدا ربات را به کانال اضافه کنید.", None
        except BotMethodInvalidError:
            return False, "این نوع دسترسی برای ربات‌ها محدود شده است. لطفاً از نام کاربری یا آیدی عددی کانال استفاده کنید.", None
        except Exception as e:
            logger.error(f"Unexpected error in validate_channel: {str(e)}")
            return False, f"خطای غیرمنتظره: لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.", None

    async def get_channel_stats(self, channel: Channel) -> dict:
        """Get basic statistics about a channel.
        
        Args:
            channel: A valid Channel object
            
        Returns:
            Dictionary containing channel statistics
        """
        try:
            full_channel = await self.client(GetFullChannelRequest(channel))
            
            return {
                'id': channel.id,
                'title': channel.title,
                'username': channel.username,
                'member_count': full_channel.full_chat.participants_count,
                'is_broadcast': channel.broadcast,  # True for channel, False for supergroup
                'is_megagroup': channel.megagroup,  # True for supergroup
                'has_geo': channel.has_geo,
                'restricted': channel.restricted,
                'verified': channel.verified,
                'scam': channel.scam,
                'fake': channel.fake,
            }
        except Exception as e:
            logger.error(f"Failed to get channel stats: {str(e)}")
            raise ValueError(f"خطا در دریافت آمار کانال: لطفاً دوباره تلاش کنید.")

    def _clean_channel_id(self, channel_id: str) -> str:
        """Clean and normalize channel ID/username.
        
        Args:
            channel_id: Raw channel identifier
            
        Returns:
            Cleaned channel identifier
        """
        if not channel_id:
            return ""
            
        # Remove whitespace
        channel_id = channel_id.strip()
        
        # Remove @ if present
        if channel_id.startswith('@'):
            channel_id = channel_id[1:]
            
        # Handle invite links
        if 't.me/' in channel_id:
            channel_id = channel_id.split('t.me/')[-1]
            if '/' in channel_id:
                channel_id = channel_id.split('/')[0]
                
        return channel_id 