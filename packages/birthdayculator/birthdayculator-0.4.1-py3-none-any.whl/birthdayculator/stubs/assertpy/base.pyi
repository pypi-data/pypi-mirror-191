from typing import Dict

from typing_extensions import Self

class BaseMixin:
    def is_equal_to(self, other: object, **kwargs: Dict[str, object]) -> Self: ...
