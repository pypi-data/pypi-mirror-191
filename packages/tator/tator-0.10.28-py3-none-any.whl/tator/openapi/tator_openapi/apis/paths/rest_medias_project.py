from tator_openapi.paths.rest_medias_project.get import ApiForget
from tator_openapi.paths.rest_medias_project.put import ApiForput
from tator_openapi.paths.rest_medias_project.post import ApiForpost
from tator_openapi.paths.rest_medias_project.delete import ApiFordelete
from tator_openapi.paths.rest_medias_project.patch import ApiForpatch


class RestMediasProject(
    ApiForget,
    ApiForput,
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
