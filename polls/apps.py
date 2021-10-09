"""Polls application configuration."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """App configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
