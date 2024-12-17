"""
ASGI config for stock_log project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
from os import environ
from strawberry.channels import GraphQLProtocolTypeRouter


environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_log.settings')
django_application = get_asgi_application()


from core.schema import schema


application = GraphQLProtocolTypeRouter(
    schema,
    django_application=django_application,
)