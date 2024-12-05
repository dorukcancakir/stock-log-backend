ACCESS_CONTROL_ALLOW_ORIGIN = b'Access-Control-Allow-Origin'
ACCESS_CONTROL_ALLOW_HEADERS = b'Access-Control-Allow-Headers'
CONTENT_TYPE = b'content-type'
DEFAULT_HEADERS = {
    ACCESS_CONTROL_ALLOW_ORIGIN,
    ACCESS_CONTROL_ALLOW_HEADERS,
    CONTENT_TYPE
}


def cors_options():
    hosts = set(b'*')
    wildcards = headers = [b'*']
    return True, hosts, wildcards, headers


class CorsMiddleware:
    def __init__(self, app):
        self.app = app
        options = cors_options()
        self.allow_all, self.hosts, self.wildcards, self.headers = options

    async def __call__(self, scope, receive, send):
        async def _base_send(event):
            if event['type'] == 'http.response.start':
                original_headers = event.get('headers') or []
                access_control_allow_origin = b'*'
                is_options = scope['method'] == 'OPTIONS'
                status = 200 if is_options else event['status']
                non_default_headers = [
                    header for header in original_headers
                    if header[0] not in DEFAULT_HEADERS
                ]
                acao = (
                    ACCESS_CONTROL_ALLOW_ORIGIN,
                    access_control_allow_origin
                )
                acah = (
                    ACCESS_CONTROL_ALLOW_HEADERS,
                    b', '.join(self.headers)
                )
                event = {
                    'type': 'http.response.start',
                    'status': status,
                    'headers': non_default_headers + [acao, acah]
                }
            await send(event)
        return await self.app(scope, receive, _base_send)
