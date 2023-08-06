import typing_extensions

from tator_openapi.apis.tags import TagValues
from tator_openapi.apis.tags.tator_api import TatorApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.TATOR: TatorApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.TATOR: TatorApi,
    }
)
