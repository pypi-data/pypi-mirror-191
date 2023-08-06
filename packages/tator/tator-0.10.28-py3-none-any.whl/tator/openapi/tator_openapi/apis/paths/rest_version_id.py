from tator_openapi.paths.rest_version_id.get import ApiForget
from tator_openapi.paths.rest_version_id.delete import ApiFordelete
from tator_openapi.paths.rest_version_id.patch import ApiForpatch


class RestVersionId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
