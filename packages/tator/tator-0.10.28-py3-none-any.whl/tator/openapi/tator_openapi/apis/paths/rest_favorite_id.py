from tator_openapi.paths.rest_favorite_id.get import ApiForget
from tator_openapi.paths.rest_favorite_id.delete import ApiFordelete
from tator_openapi.paths.rest_favorite_id.patch import ApiForpatch


class RestFavoriteId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
