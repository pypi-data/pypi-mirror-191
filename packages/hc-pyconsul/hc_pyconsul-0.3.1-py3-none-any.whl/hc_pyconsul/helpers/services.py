import re

from hc_pyconsul.models.helpers import NomadAllocation


def extract_alloc_id_from_service_name(service_id: str) -> NomadAllocation:
    """
    Extracts the Nomad allocation ID from a Consul service name.

    Parameters
    ----------
    service_id: str

    Returns
    -------
    alloc_id: NomadAllocation

    Raises
    ------
    FailedExtractingAllocID
    """

    alloc_id = NomadAllocation()

    full_id = re.match(r'^_nomad-task-(\w+-\w+-\w+-\w+-\w+)', service_id)

    if not full_id:
        return alloc_id

    try:
        full_id_groups = full_id.groups()[0].split('-')
        alloc_id = NomadAllocation(id=full_id_groups[0], id_long='-'.join(full_id_groups))
    except AttributeError:
        # Gracefully exit and allow default values of empty strings be provided.
        pass

    return alloc_id
