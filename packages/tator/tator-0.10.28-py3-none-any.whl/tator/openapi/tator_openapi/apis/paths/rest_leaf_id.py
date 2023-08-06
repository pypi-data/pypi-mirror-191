from tator_openapi.paths.rest_leaf_id.get import ApiForget
from tator_openapi.paths.rest_leaf_id.delete import ApiFordelete
from tator_openapi.paths.rest_leaf_id.patch import ApiForpatch


class RestLeafId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
