from tator_openapi.paths.rest_organization_id.get import ApiForget
from tator_openapi.paths.rest_organization_id.delete import ApiFordelete
from tator_openapi.paths.rest_organization_id.patch import ApiForpatch


class RestOrganizationId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
