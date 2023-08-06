from tator_openapi.paths.rest_project_id.get import ApiForget
from tator_openapi.paths.rest_project_id.delete import ApiFordelete
from tator_openapi.paths.rest_project_id.patch import ApiForpatch


class RestProjectId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
