from tator_openapi.paths.rest_attribute_type_id.put import ApiForput
from tator_openapi.paths.rest_attribute_type_id.post import ApiForpost
from tator_openapi.paths.rest_attribute_type_id.delete import ApiFordelete
from tator_openapi.paths.rest_attribute_type_id.patch import ApiForpatch


class RestAttributeTypeId(
    ApiForput,
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
