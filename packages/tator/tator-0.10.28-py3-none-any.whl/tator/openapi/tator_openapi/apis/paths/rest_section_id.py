from tator_openapi.paths.rest_section_id.get import ApiForget
from tator_openapi.paths.rest_section_id.delete import ApiFordelete
from tator_openapi.paths.rest_section_id.patch import ApiForpatch


class RestSectionId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
