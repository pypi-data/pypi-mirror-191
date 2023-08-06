from __future__ import annotations

from logging import Logger
from typing import Optional

from assertpy.base import BaseMixin
from assertpy.collection import CollectionMixin
from assertpy.contains import ContainsMixin
from assertpy.date import DateMixin
from assertpy.dict import DictMixin
from assertpy.dynamic import DynamicMixin
from assertpy.exception import ExceptionMixin
from assertpy.extracting import ExtractingMixin
from assertpy.file import FileMixin
from assertpy.helpers import HelpersMixin
from assertpy.numeric import NumericMixin
from assertpy.snapshot import SnapshotMixin
from assertpy.string import StringMixin

def assert_that(val: object, description: Optional[str] = "") -> AssertionBuilder: ...

class AssertionBuilder(
    StringMixin,
    SnapshotMixin,
    NumericMixin,
    HelpersMixin,
    FileMixin,
    ExtractingMixin,
    ExceptionMixin,
    DynamicMixin,
    DictMixin,
    DateMixin,
    ContainsMixin,
    CollectionMixin,
    BaseMixin,
    object,
):
    def __init__(
        self,
        val: object,
        description: Optional[str] = "",
        kind: Optional[str] = None,
        expected: Optional[Exception] = None,
        logger: Optional[Logger] = None,
    ) -> None: ...
    def builder(
        self,
        val: object,
        description: Optional[str] = "",
        kind: Optional[str] = None,
        expected: Optional[Exception] = None,
        logger: Optional[Logger] = None,
    ) -> AssertionBuilder: ...
    def error(self, msg: str) -> None: ...
