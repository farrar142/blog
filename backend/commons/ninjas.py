from typing import TYPE_CHECKING, Any, Generic, TypeVar, TypedDict
from ninja.patch_dict import PatchDictUtil, Annotated


T = TypeVar("T")


class _PatchDict[T](dict):
    pass


if TYPE_CHECKING:
    PatchDict = _PatchDict
else:
    PatchDict = PatchDictUtil()
