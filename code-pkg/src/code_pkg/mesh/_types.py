from typing import TYPE_CHECKING, Literal, Required

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path

    from cheartpy.fe.aliases import TopologyDef
    from pytools.arrays import ToFloat, ToInt

type TopologyType = Literal[
    "Disp", "Pres", "Inlet", "Outlet", "Inner", "Outer", "Brachial", "Carotid", "Subclavian"
]
type DissectedType = Literal[
    "Disp",
    "Pres",
    "Inlet",
    "Outlet",
    "Inner",
    "Outer",
    "Brachial",
    "Carotid",
    "Subclavian",
    "ca1",
    "ca2",
    "ca3",
]


class CylinderDef(TypedDict, total=False):
    """Definition of a cylinder mesh.

    Struct
    ------
    size
        The number of elements in each direction (r, q, z).
    shape
        The physical dimensions of the cylinder (rin, rout, length).
    offset
        The offset of the inner surface from the centerline, as a fraction of the wall thickness.
        Default is 0.0 (left aligned).
    orientation
        The axis along which the cylinder is oriented. Must be one of "x", "y", or "z".
        Default is "z".

    """

    size: Required[tuple[ToInt, ToInt, ToInt]]
    shape: Required[tuple[ToFloat, ToFloat, ToFloat]]
    offset: ToFloat
    orientation: Literal["x", "y", "z"]
    warp: bool


class AortaDef(TypedDict, total=False):
    """Definition of an aorta mesh.

    Struct
    ------
    name: str
        The name of the aorta mesh.
    """

    name: str


type GeoDef = CylinderDef | AortaDef
type ElementTypes = Literal["hex", "tet"]
_TOPS = Literal[
    "Disp", "Pres", "Inlet", "Outlet", "Inner", "Outer", "Brachial", "Carotid", "Subclavian"
]
_FIELDS = Literal["a_z", "center", "fiber"]
_BNDS = Literal["Inlet", "Outlet", "Inner", "Outer", "Brachial", "Carotid", "Subclavian"]


class BndTag(TypedDict, total=True):
    name: str
    tag: int


class TopSpec(TypedDict, total=True):
    prefix: str
    elem: ElementTypes
    order: int


class FieldTags(TypedDict, total=True):
    """Definition of field tags.

    Parameters
    ----------
    a_z
        The tag for the centerline field.
    center
        The tag for the center position field.
    fiber
        The tag for the fiber direction field.
    a_c
        The tag for the aorta coordinate field.

    """

    a_z: str
    a_r: str
    a_c: str
    Z: str
    R: str
    C: str


class MeshDef(TypedDict, total=False):
    """Definition of a mesh.

    Parameters
    ----------
    cylinder
        The definition of the cylinder mesh.

    """

    geo: Required[GeoDef]
    home: Required[Path]
    top: Required[Mapping[_TOPS, TopSpec]]
    fields: Required[FieldTags]
    bnds: Required[Mapping[_BNDS, BndTag]]
    space: str


class MeshDefN[T](TypedDict, total=False):
    """Definition of a mesh.

    Parameters
    ----------
    cylinder
        The definition of the cylinder mesh.

    """

    label: Sequence[T]
    geo: Required[GeoDef]
    home: Required[Path]
    top: Required[Mapping[T, TopologyDef[T]]]
    fields: Required[FieldTags]
    bnds: Required[Mapping[T, BndTag]]
    space: str
