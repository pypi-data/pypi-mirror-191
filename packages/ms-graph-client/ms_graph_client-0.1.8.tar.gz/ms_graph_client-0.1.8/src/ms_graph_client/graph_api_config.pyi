class GraphAPIConfig:
    client_id: str
    tenant_id: str
    client_secret: str
    api_url: str
    def __init__(self, client_id: str, tenant_id: str, client_secret: str, api_url: str) -> None: ...
