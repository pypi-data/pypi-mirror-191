from typing import List, Union, Any, TypeVar
from typing_extensions import TypeGuard
from enum import Enum

T = TypeVar("T", bound=Enum)


def list_to_filter(field_name: str, items: Union[List[str], List[T], str, T]) -> str:
    if isinstance(items, str):
        return f'{field_name}: "{items}"'
    if isinstance(items, Enum):
        return f'{field_name}: "{items.value}"'

    if is_enum_list(items):
        n_items: List[str] = [x.value for x in items]
        n_items = ['"' + x + '"' for x in n_items]
        return f"{field_name} IN ({','.join(n_items)})"
    elif is_str_list(items):
        n_items = ['"' + x + '"' for x in items]
        return f"{field_name} IN ({','.join(n_items)})"

    raise TypeError("not supported")


def is_enum_list(lst: List[Any]) -> TypeGuard[List[Enum]]:
    return all(isinstance(x, Enum) for x in lst)


def is_str_list(lst: List[Any]) -> TypeGuard[List[str]]:
    return all(isinstance(x, str) for x in lst)
