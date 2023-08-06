from django.conf import settings


class Config:
    BLOG_PAGINATION = int(getattr(settings, "BLOGORAMA_BLOG_PAGINATION", "5"))
    DEFAULT_LANGUAGE_CODE = getattr(settings, "BLOGORAMA_DEFAULT_LANGUAGE_CODE", "en")
