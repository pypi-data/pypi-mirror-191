from tator_openapi.paths.rest_algorithm_id.get import ApiForget
from tator_openapi.paths.rest_algorithm_id.delete import ApiFordelete
from tator_openapi.paths.rest_algorithm_id.patch import ApiForpatch


class RestAlgorithmId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
