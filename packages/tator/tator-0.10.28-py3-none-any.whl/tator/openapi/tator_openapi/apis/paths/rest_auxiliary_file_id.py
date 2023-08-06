from tator_openapi.paths.rest_auxiliary_file_id.get import ApiForget
from tator_openapi.paths.rest_auxiliary_file_id.delete import ApiFordelete
from tator_openapi.paths.rest_auxiliary_file_id.patch import ApiForpatch


class RestAuxiliaryFileId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
