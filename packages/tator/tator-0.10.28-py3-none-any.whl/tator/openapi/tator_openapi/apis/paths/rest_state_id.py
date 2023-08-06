from tator_openapi.paths.rest_state_id.get import ApiForget
from tator_openapi.paths.rest_state_id.delete import ApiFordelete
from tator_openapi.paths.rest_state_id.patch import ApiForpatch


class RestStateId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
