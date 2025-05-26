class ChannelManagementError(Exception):
    """Base exception for channel management"""
    pass

class ChannelNotFoundError(ChannelManagementError):
    """Raised when channel is not found"""
    pass

class NotAdminError(ChannelManagementError):
    """Raised when bot is not admin in channel"""
    pass

class InvalidChannelError(ChannelManagementError):
    """Raised when channel link/id is invalid"""
    pass
