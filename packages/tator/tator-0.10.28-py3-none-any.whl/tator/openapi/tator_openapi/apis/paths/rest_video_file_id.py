from tator_openapi.paths.rest_video_file_id.get import ApiForget
from tator_openapi.paths.rest_video_file_id.delete import ApiFordelete
from tator_openapi.paths.rest_video_file_id.patch import ApiForpatch


class RestVideoFileId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
