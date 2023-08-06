import os
from typing import Any
from typing import Optional

import httpx
from pydantic.dataclasses import dataclass

from hc_pyconsul.exceptions import Unauthenticated
from hc_pyconsul.exceptions import UnknownResourceCalled


@dataclass
class ConsulAPI:
    address: str = "http://localhost:8500"
    token: Optional[str] = None
    namespace: Optional[str] = None
    timeout: int = 15

    def __post_init__(self):

        if os.environ.get('CONSUL_HTTP_ADDR'):
            self.address = os.environ.get('CONSUL_HTTP_ADDR')

        if os.environ.get('CONSUL_HTTP_TOKEN'):
            self.token = os.environ.get('CONSUL_HTTP_TOKEN')

        if os.environ.get('CONSUL_NAMESPACE'):
            self.namespace = os.environ.get('CONSUL_NAMESPACE')

    def call_api(self, endpoint: str, verb: str, **kwargs) -> Any:
        """
        Generic method to make API calls.

        Parameters
        ----------
        endpoint: str
        verb: str
        span=None

        Returns
        -------
        return_data: Union[str, dict, list]

        Raises
        ------
        exceptions.Unauthenticated
        exceptions.UnknownResourceCalled
        """

        headers = kwargs.get('headers', {})
        if self.token:
            headers.update(
                {
                    'X-Consul-Token': self.token
                }
            )
        kwargs['timeout'] = self.timeout

        if self.namespace:
            if not kwargs.get('params'):
                kwargs['params'] = {}

            kwargs['params'].update({'namespace': self.namespace})

        url = f'{self.address}/v1{endpoint}'

        try:
            request: httpx.Response = getattr(httpx, verb.lower())(
                url, headers=headers, **kwargs
            )

            request.raise_for_status()
        except httpx.HTTPStatusError as request_error:
            status_code = request_error.response.status_code

            if status_code == 403:
                raise Unauthenticated('API called failed to due being unauthenticated. Maybe your token expired?')
            if status_code == 404:
                raise UnknownResourceCalled('Received a 404. Check supported API endpoints for your version of Consul.')

            raise request_error

        # Dynamically return the appropriate type.
        string_types = ['text/plain', 'application/octet-stream']
        if request.headers['content-type'] in string_types:
            return_data = request.text
        else:
            return_data = request.json()

        return return_data
