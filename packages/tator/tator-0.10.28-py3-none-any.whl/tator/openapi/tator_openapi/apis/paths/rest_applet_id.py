from tator_openapi.paths.rest_applet_id.get import ApiForget
from tator_openapi.paths.rest_applet_id.delete import ApiFordelete
from tator_openapi.paths.rest_applet_id.patch import ApiForpatch


class RestAppletId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
