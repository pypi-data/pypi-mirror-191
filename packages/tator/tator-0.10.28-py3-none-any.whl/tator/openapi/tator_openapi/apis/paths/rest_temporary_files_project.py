from tator_openapi.paths.rest_temporary_files_project.get import ApiForget
from tator_openapi.paths.rest_temporary_files_project.post import ApiForpost
from tator_openapi.paths.rest_temporary_files_project.delete import ApiFordelete


class RestTemporaryFilesProject(
    ApiForget,
    ApiForpost,
    ApiFordelete,
):
    pass
