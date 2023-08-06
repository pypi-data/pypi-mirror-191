class GraphAPIConfig:
    def __init__(self, client_id: str, tenant_id: str, client_secret: str, api_url: str):
        self.client_id: str = client_id
        self.tenant_id: str = tenant_id
        self.client_secret: str = client_secret
        self.api_url: str = api_url.rstrip("/")
