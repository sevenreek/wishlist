from secrets import token_bytes
import base64

from ..config import settings

DEFAULT_SLUG_UNIQUENESS_ATTEMPTS = 3

def generate_wishlist_slug(length=settings.wishlist_slug_length) -> str:
    return base64.b32encode(token_bytes(length))[:length].decode('utf-8')
