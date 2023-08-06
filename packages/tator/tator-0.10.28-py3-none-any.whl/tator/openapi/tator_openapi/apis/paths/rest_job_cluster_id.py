from tator_openapi.paths.rest_job_cluster_id.get import ApiForget
from tator_openapi.paths.rest_job_cluster_id.delete import ApiFordelete
from tator_openapi.paths.rest_job_cluster_id.patch import ApiForpatch


class RestJobClusterId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
