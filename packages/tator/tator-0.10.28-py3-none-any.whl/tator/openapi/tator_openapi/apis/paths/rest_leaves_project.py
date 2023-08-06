from tator_openapi.paths.rest_leaves_project.get import ApiForget
from tator_openapi.paths.rest_leaves_project.put import ApiForput
from tator_openapi.paths.rest_leaves_project.post import ApiForpost
from tator_openapi.paths.rest_leaves_project.delete import ApiFordelete
from tator_openapi.paths.rest_leaves_project.patch import ApiForpatch


class RestLeavesProject(
    ApiForget,
    ApiForput,
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
