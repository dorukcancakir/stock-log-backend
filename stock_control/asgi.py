"""
ASGI config for stock_control project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
from os import environ
from strawberry.channels import GraphQLProtocolTypeRouter
from core.middlewares import CorsMiddleware


environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_control.settings')
django_application = get_asgi_application()


from core.schema import schema


application = GraphQLProtocolTypeRouter(
    schema,
    django_application=django_application,
)
application = CorsMiddleware(application)
