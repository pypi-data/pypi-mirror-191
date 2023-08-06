"""Implementation of attrs/dataclasses' fields and methods.

This is a transitional module for those who want to write code that works across
versions of this library, or need configuration and can't use type instances on
Python 3.10+.
"""

from typing import Any
from typing import BinaryIO
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import attr

from binobj.fields.base import Field
from binobj.fields.base import NOT_PRESENT
from binobj.fields.base import UNDEFINED
from binobj.fields.base import _Undefined
from binobj.fields.base import _Default
from binobj.fields.base import _NotPresent
from binobj.typedefs import FieldValidator
from binobj.typedefs import StrDict


T = TypeVar("T")


def field(type_: Optional[Type[Field]] = None, **kwargs: Any):
    """Create a field."""
