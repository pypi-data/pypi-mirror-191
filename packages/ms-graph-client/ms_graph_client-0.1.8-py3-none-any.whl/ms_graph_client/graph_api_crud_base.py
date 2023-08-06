from .graph_api_config import GraphAPIConfig
import requests
from requests.adapters import HTTPAdapter, Retry
import cachetools.func
from typing import Optional, Any


class GraphAPICRUDBASE:
    def __init__(self, config: GraphAPIConfig, session: Optional[requests.Session] = None):
        self.config = config

        if session is None:
            self.session: requests.Session = self._default_session()
        else:
            self.session: requests.Session = session

    def _default_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            connect=3,
            allowed_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
            status_forcelist=[429],
            backoff_factor=0.5,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _combine_url(self, url_part: str) -> str:
        if "https://" in url_part:
            return url_part
        else:
            return self.config.api_url + "/" + url_part.strip("/")

    # By default token expires in 3600 seconds - we are renewing 1/2 of the way through
    # Hard coding so we dont have to track time?
    def _non_cacheable_token_call(self) -> Any:
        """
        https://learn.microsoft.com/en-us/graph/auth-v2-service#4-get-an-access-token

        POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token HTTP/1.1
                Host: login.microsoftonline.com
                Content-Type: application/x-www-form-urlencoded

                client_id=535fb089-9ff3-47b6-9bfb-4f1264799865
                &scope=https%3A%2F%2Fgraph.microsoft.com%2F.default
                &client_secret=qWgdYAmab0YSkuL1qKv5bPX
                &grant_type=client_credentials

        """

        str = "https://login.microsoftonline.com/" + self.config.tenant_id + "/oauth2/v2.0/token"
        d = {
            "client_id": self.config.client_id,
            "scope": "https://graph.microsoft.com/.default",
            "client_secret": self.config.client_secret,
            "grant_type": "client_credentials",
        }

        s = requests.post(url=str, data=d)
        s.raise_for_status()
        return s.json()

    @cachetools.func.ttl_cache(maxsize=5, ttl=1800)
    def _token_call(self) -> Any:
        return self._non_cacheable_token_call()

    def _response_has_json(self, response: requests.Response) -> bool:
        return response.headers.get("Content-Type", "").startswith("application/json")

    def validate_credentials(self) -> None:
        self._non_cacheable_token_call()

    def _call(
        self,
        url: str,
        body: Optional[Any],
        json: Optional[Any],
        method: str,
        extra_headers: Optional[Any] = None,
    ) -> Any:

        if extra_headers is None:
            extra_headers = {}

        # Pull in a fresh token
        t_resp = self._token_call()

        api_response = None

        if "ConsistencyLevel" not in extra_headers.keys():
            extra_headers.update({"ConsistencyLevel": "eventual"})

        try:
            api_response = self.session.request(
                url=url,
                method=method,
                headers={"Authorization": f'{t_resp["token_type"]} {t_resp["access_token"]}', **extra_headers},
                data=body,
                json=json,
            )

            api_response.raise_for_status()

            if self._response_has_json(api_response):
                return api_response.json()
            else:
                return api_response

        except requests.exceptions.RequestException as e:
            reason = f"Request failed. Reason [{e}]"
            if api_response is not None:
                if self._response_has_json(api_response):
                    reason += f"\n{api_response.json()}"
            raise Exception(reason) from e

    def _get(
        self, url_part: str, json: Optional[Any] = None, body: Optional[Any] = None, extra_headers: Optional[Any] = None
    ) -> Any:
        return self._call(
            url=self._combine_url(url_part=url_part), body=body, method="GET", extra_headers=extra_headers, json=json
        )

    def _post(
        self, url_part: str, json: Optional[Any] = None, body: Optional[Any] = None, extra_headers: Optional[Any] = None
    ) -> Any:
        return self._call(
            url=self._combine_url(url_part=url_part), body=body, method="POST", extra_headers=extra_headers, json=json
        )

    def _put(
        self, url_part: str, json: Optional[Any] = None, body: Optional[Any] = None, extra_headers: Optional[Any] = None
    ) -> Any:
        return self._call(
            url=self._combine_url(url_part=url_part), body=body, method="PUT", extra_headers=extra_headers, json=json
        )

    def _patch(
        self, url_part: str, json: Optional[Any] = None, body: Optional[Any] = None, extra_headers: Optional[Any] = None
    ) -> Any:
        return self._call(
            url=self._combine_url(url_part=url_part), body=body, method="PATCH", extra_headers=extra_headers, json=json
        )

    def _delete(
        self, url_part: str, json: Optional[Any] = None, body: Optional[Any] = None, extra_headers: Optional[Any] = None
    ) -> Any:
        return self._call(
            url=self._combine_url(url_part=url_part), body=body, method="DELETE", extra_headers=extra_headers, json=json
        )
