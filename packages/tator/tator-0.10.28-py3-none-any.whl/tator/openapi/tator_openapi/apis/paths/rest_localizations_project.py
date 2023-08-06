from tator_openapi.paths.rest_localizations_project.get import ApiForget
from tator_openapi.paths.rest_localizations_project.put import ApiForput
from tator_openapi.paths.rest_localizations_project.post import ApiForpost
from tator_openapi.paths.rest_localizations_project.delete import ApiFordelete
from tator_openapi.paths.rest_localizations_project.patch import ApiForpatch


class RestLocalizationsProject(
    ApiForget,
    ApiForput,
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
