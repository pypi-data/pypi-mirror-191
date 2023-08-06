from tator_openapi.paths.rest_membership_id.get import ApiForget
from tator_openapi.paths.rest_membership_id.delete import ApiFordelete
from tator_openapi.paths.rest_membership_id.patch import ApiForpatch


class RestMembershipId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
