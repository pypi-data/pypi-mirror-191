import typing as ty
import attrs
from fileformats.core import DataType
from fileformats.generic import File
from fileformats.field import Singluar
from fileformats.core.mixin import WithQualifiers


class FileClassifier(DataType):
    pass


class A(FileClassifier):
    pass


class B(FileClassifier):
    pass


class C(FileClassifier):
    pass


class D(FileClassifier):
    pass


class E(C):
    pass


class F(WithQualifiers, File):
    qualifiers_attr_name = "content_types"
    content_types = ()
    ext = ".f"


class G(F):
    ext = ".g"


class H(WithQualifiers, File):
    qualifiers_attr_name = "content_types"
    content_types = ()
    ext = ".h"

    allowed_qualifiers = (A, B, C)


class J(H):
    ext = ".j"


class K(WithQualifiers, File):

    ext = ".k"
    qualifiers_attr_name = "new_qualifiers_attr"
    new_qualifiers_attr = ()
    ordered_qualifiers = True


class L(WithQualifiers, File):

    ext = ".l"
    qualifiers_attr_name = "new_qualifiers_attr"
    new_qualifiers_attr = ()
    ordered_qualifiers = True


class M(WithQualifiers, File):
    qualifiers_attr_name = "content_types"
    content_types = None  # Should be None not ()
    ext = ".m"
    multiple_qualifiers = False


class N(WithQualifiers, File):
    qualifiers_attr_name = "content_types"
    content_types = ()
    ext = ".n"


@attrs.define
class TestField(Singluar):

    value: ty.Any


class P(WithQualifiers, File):
    ext = ".p"
    qualifiers_attr_name = "content_types"
    content_types = ()


class Q(WithQualifiers, File):
    ext = ".z"
    qualifiers_attr_name = "new_qualifiers_attr"
    # MISSING default value for "new_qualifiers_attr"


class R(WithQualifiers, File):

    ext = ".r"
    qualifiers_attr_name = "new_qualifiers_attr"
    new_qualifiers_attr = ()
    ordered_qualifiers = True
