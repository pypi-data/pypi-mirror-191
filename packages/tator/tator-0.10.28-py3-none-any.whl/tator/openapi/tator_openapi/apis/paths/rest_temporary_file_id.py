from tator_openapi.paths.rest_temporary_file_id.get import ApiForget
from tator_openapi.paths.rest_temporary_file_id.delete import ApiFordelete


class RestTemporaryFileId(
    ApiForget,
    ApiFordelete,
):
    pass
