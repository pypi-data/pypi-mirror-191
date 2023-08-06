"""Module exceptions."""


class BitrixError(Exception):
    """Main bitrix error."""


class BadBitrixResponseError(BitrixError):
    """Bad response from bx24."""


class BatchError(BitrixError):
    """Rises if batch size is more than 50."""
