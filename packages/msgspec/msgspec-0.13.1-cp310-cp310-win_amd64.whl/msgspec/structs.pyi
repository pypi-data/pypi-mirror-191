from typing import Any, TypeVar

from . import Struct

S = TypeVar("S", bound=Struct, covariant=True)

def replace(struct: S, /, **changes: Any) -> S: ...
def asdict(struct: Struct) -> dict: ...
def astuple(struct: Struct) -> tuple: ...
