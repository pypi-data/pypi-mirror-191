from pydantic.dataclasses import dataclass

from hc_pyconsul.lib.consul import ConsulAPI
from hc_pyconsul.lib.tracing import tracing
from hc_pyconsul.models.health import ServiceHealth


@dataclass
class ConsulHealth(ConsulAPI):

    # pylint: disable=too-many-arguments,invalid-name
    @tracing('List Service Instances')
    def list_service_instances(
        self, service: str, dc: str = None, near: str = None, tag: str = None,
        node_meta: str = None, passing: bool = False, filter_expression: str = None,
        peer: str = None, ns: str = None
    ) -> list[ServiceHealth]:
        """
        API Reference:
            https://developer.hashicorp.com/consul/api-docs/health#list-nodes-for-service

        Parameters
        ----------
        service: str
        dc: str = None
        near: str = None
        tag: str = None
        node_meta: str = None
        passing: bool = False
        filter_expression: str = None
            Name differs from API query param to avoid conflict w/ built-in filter.
        peer: str = None
        ns: str = None

        Returns
        -------
        services: list[ServiceHealth]
            List of services.
        """

        params: dict = {}

        if dc:
            params['dc'] = dc
        if near:
            params['near'] = near
        if tag:
            params['tag'] = tag
        if node_meta:
            params['node-meta'] = node_meta
        if passing:
            params['passing'] = passing
        if filter_expression:
            params['filter'] = filter_expression
        if peer:
            params['peer'] = peer
        if ns:
            params['ns'] = ns

        results = self.call_api(endpoint=f'/health/service/{service}', verb='GET', params=params)
        services: list[ServiceHealth] = [ServiceHealth.parse_obj(item) for item in results]

        return services
