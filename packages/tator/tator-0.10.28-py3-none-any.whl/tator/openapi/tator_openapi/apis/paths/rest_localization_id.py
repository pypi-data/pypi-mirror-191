from tator_openapi.paths.rest_localization_id.get import ApiForget
from tator_openapi.paths.rest_localization_id.delete import ApiFordelete
from tator_openapi.paths.rest_localization_id.patch import ApiForpatch


class RestLocalizationId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
