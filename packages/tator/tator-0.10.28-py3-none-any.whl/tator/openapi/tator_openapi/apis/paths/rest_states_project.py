from tator_openapi.paths.rest_states_project.get import ApiForget
from tator_openapi.paths.rest_states_project.put import ApiForput
from tator_openapi.paths.rest_states_project.post import ApiForpost
from tator_openapi.paths.rest_states_project.delete import ApiFordelete
from tator_openapi.paths.rest_states_project.patch import ApiForpatch


class RestStatesProject(
    ApiForget,
    ApiForput,
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
