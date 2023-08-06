from tator_openapi.paths.rest_affiliation_id.get import ApiForget
from tator_openapi.paths.rest_affiliation_id.delete import ApiFordelete
from tator_openapi.paths.rest_affiliation_id.patch import ApiForpatch


class RestAffiliationId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
