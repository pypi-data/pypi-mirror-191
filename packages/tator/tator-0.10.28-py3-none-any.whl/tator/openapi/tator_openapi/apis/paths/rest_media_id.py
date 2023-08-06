from tator_openapi.paths.rest_media_id.get import ApiForget
from tator_openapi.paths.rest_media_id.delete import ApiFordelete
from tator_openapi.paths.rest_media_id.patch import ApiForpatch


class RestMediaId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
