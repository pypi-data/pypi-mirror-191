from tator_openapi.paths.rest_leaf_type_id.get import ApiForget
from tator_openapi.paths.rest_leaf_type_id.delete import ApiFordelete
from tator_openapi.paths.rest_leaf_type_id.patch import ApiForpatch


class RestLeafTypeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
