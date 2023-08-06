from tator_openapi.paths.rest_bookmark_id.get import ApiForget
from tator_openapi.paths.rest_bookmark_id.delete import ApiFordelete
from tator_openapi.paths.rest_bookmark_id.patch import ApiForpatch


class RestBookmarkId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
