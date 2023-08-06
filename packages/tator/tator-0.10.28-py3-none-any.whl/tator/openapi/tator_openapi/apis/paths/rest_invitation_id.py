from tator_openapi.paths.rest_invitation_id.get import ApiForget
from tator_openapi.paths.rest_invitation_id.delete import ApiFordelete
from tator_openapi.paths.rest_invitation_id.patch import ApiForpatch


class RestInvitationId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
