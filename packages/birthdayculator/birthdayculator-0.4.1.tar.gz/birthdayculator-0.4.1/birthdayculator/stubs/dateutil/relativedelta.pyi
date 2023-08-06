from __future__ import annotations

from datetime import date, timedelta
from typing import Optional, TypeAlias, Union, overload

from typing_extensions import Self

RelativeDeltaCompat: TypeAlias = Union[timedelta, date]

class relativedelta(object):
    years: int
    months: int
    days: int
    leapdays: int
    hours: int
    minutes: int
    seconds: int
    microseconds: int
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    weekday: Optional[int]
    hour: Optional[int]
    minute: Optional[int]
    second: Optional[int]
    microsecond: Optional[int]
    _has_time: int

    def __init__(
        self,
        dt1: Optional[date] = None,
        dt2: Optional[date] = None,
        years: int = 0,
        months: int = 0,
        days: int = 0,
        leapdays: int = 0,
        weeks: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        microseconds: int = 0,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        weekday: Optional[int] = None,
        yearday: Optional[int] = None,
        nlyearday: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        microsecond: Optional[int] = None,
    ) -> None: ...
    def _fix(self) -> None: ...
    @overload
    def weeks(self) -> int: ...
    @weeks.setter
    def weeks(self, value: int) -> None: ...
    def _set_months(self, months: int) -> None: ...
    def normalized(self) -> Self: ...
    def __add__(self, other: Union[Self, RelativeDeltaCompat]) -> Self: ...
    def __radd__(self, other: Union[Self, RelativeDeltaCompat]) -> Self: ...
    def __rsub__(self, other: Union[Self, RelativeDeltaCompat]) -> Self: ...
    def __sub__(self, other: Union[Self, RelativeDeltaCompat]) -> Self: ...
    def __abs__(self) -> Self: ...
    def __neg__(self) -> Self: ...
    def __bool__(self) -> bool: ...
    # Compatibility with Python 2.x
    __nonzero__ = __bool__

    def __mul__(self, other: Union[Self, RelativeDeltaCompat]) -> Self: ...
    __rmul__ = __mul__
    def __eq__(self, other: Union[Self, RelativeDeltaCompat]) -> Self: ...
    def __hash__(self) -> int: ...
    def __ne__(self, other: Union[Self, RelativeDeltaCompat]) -> bool: ...
    def __div__(self, other: Union[Self, RelativeDeltaCompat]) -> Self: ...
    __truediv__ = __div__

    def __repr__(self) -> str: ...

def _sign(x: float) -> int: ...
