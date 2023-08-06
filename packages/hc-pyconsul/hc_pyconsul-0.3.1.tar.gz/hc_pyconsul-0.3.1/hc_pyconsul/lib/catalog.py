from pydantic.dataclasses import dataclass

from hc_pyconsul.lib.consul import ConsulAPI
from hc_pyconsul.lib.tracing import tracing


@dataclass
class ConsulCatalog(ConsulAPI):
    endpoint = 'catalog'

    # pylint: disable=invalid-name
    @tracing('List Services')
    def list_services(self, dc: str = None, node_meta: list[str] = None, namespace: str = None) -> dict[str, list[str]]:
        """
        Link to official docs:
            https://developer.hashicorp.com/consul/api-docs/catalog#list-services

        Parameters
        ----------
        dc: str = None
            Specifies the datacenter to query.
            This will default to the datacenter of the agent being queried.
        node_meta: list[str] = None
            Specifies a desired node metadata key/value in the form of key:value.
            This parameter can be specified multiple times,
            and filters the results to nodes with the specified key/value pairs.
        namespace: str = None
            Enterprise Only
            Specifies the namespace of the services you lookup.

        Returns
        -------
        services: dict[str, list[str]]
            The list[str] is the tags for the given service.

        """
        params = {}
        if dc:
            params.update({
                'dc': dc
            })

        if node_meta:
            params.update({
                'node-meta': ','.join(meta_item for meta_item in node_meta)
            })

        if namespace:
            params.update({
                'ns': namespace
            })

        results = self.call_api(endpoint=f'/{self.endpoint}/services', verb='GET', params=params)

        return results
