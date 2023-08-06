from tator_openapi.paths.rest_analysis_id.get import ApiForget
from tator_openapi.paths.rest_analysis_id.delete import ApiFordelete
from tator_openapi.paths.rest_analysis_id.patch import ApiForpatch


class RestAnalysisId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
