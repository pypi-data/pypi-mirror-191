from tator_openapi.paths.rest_localization_type_id.get import ApiForget
from tator_openapi.paths.rest_localization_type_id.delete import ApiFordelete
from tator_openapi.paths.rest_localization_type_id.patch import ApiForpatch


class RestLocalizationTypeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
