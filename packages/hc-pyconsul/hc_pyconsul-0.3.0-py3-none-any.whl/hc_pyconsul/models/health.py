from pydantic import BaseModel
from pydantic import Field

from hc_pyconsul.helpers.services import extract_alloc_id_from_service_name
from hc_pyconsul.models.helpers import NomadAllocation


class HealthCheck(BaseModel):
    node: str = Field(..., alias='Node')
    check_id: str = Field(..., alias='CheckID')
    name: str = Field(..., alias='Name')
    status: str = Field(..., alias='Status')
    notes: str = Field(..., alias='Notes')
    output: str = Field(..., alias='Output')
    service_id: str = Field(..., alias='ServiceID')
    service_name: str = Field(..., alias='ServiceName')
    service_tags: list[str] = Field(..., alias='ServiceTags')
    namespace: str = Field(..., alias='Namespace')


class HealthWeights(BaseModel):
    passing: int = Field(..., alias='Passing')
    warning: int = Field(..., alias='Warning')


class NodeTaggedAddresses(BaseModel):
    lan: str = Field(..., alias='lan')
    wan: str = Field(..., alias='wan')


class ServiceNode(BaseModel):
    id: str = Field(..., alias='ID')
    node: str = Field(..., alias='Node')
    address: str = Field(..., alias='Address')
    datacenter: str = Field(..., alias='Datacenter')
    tagged_addresses: NodeTaggedAddresses = Field(..., alias='TaggedAddresses')
    meta: dict = Field(default_factory=dict, alias='Meta')


class TaggedAddress(BaseModel):
    address: str = Field(..., alias='address')
    port: int = Field(..., alias='port')


class ServiceTaggedAddresses(BaseModel):
    lan: TaggedAddress = Field(..., alias='lan')
    wan: TaggedAddress = Field(..., alias='wan')


class Service(BaseModel):
    id: str = Field(..., alias='ID')
    service: str = Field(..., alias='Service')
    tags: list[str] = Field(..., alias='Tags')
    address: str = Field(..., alias='Address')
    tagged_addresses: ServiceTaggedAddresses = Field(..., alias='TaggedAddresses')
    meta: dict = Field(default_factory=dict, alias='Meta')
    port: int = Field(..., alias='Port')
    weights: HealthWeights = Field(..., alias='Weights')
    namespace: str = Field(..., alias='Namespace')


class ServiceHealth(BaseModel):
    node: ServiceNode = Field(..., alias='Node')
    service: Service = Field(..., alias='Service')
    checks: list[HealthCheck] = Field(default_factory=list, alias='Checks')

    @property
    def alloc_id(self) -> NomadAllocation:
        """Attempts to extract out the Nomad allocation ID for the given service check."""

        return extract_alloc_id_from_service_name(service_id=self.service.id)
