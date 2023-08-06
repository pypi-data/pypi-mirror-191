from tator_openapi.paths.rest_bucket_id.get import ApiForget
from tator_openapi.paths.rest_bucket_id.delete import ApiFordelete
from tator_openapi.paths.rest_bucket_id.patch import ApiForpatch


class RestBucketId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
