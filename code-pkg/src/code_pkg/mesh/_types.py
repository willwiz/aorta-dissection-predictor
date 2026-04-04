from typing import TYPE_CHECKING, Literal, Required

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from pytools.arrays import ToFloat, ToInt


class CylinderDef(TypedDict, total=False):
    """Definition of a cylinder mesh.

    Parameters
    ----------
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


type GeoDef = CylinderDef
type ElementTypes = Literal["hex", "tet"]
_TOPS = Literal["Disp", "Pres"]
_FIELDS = Literal["cl", "center", "fiber"]
_BNDS = Literal["Inlet", "Outlet", "Inner", "Outer"]


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
    cl
        The tag for the centerline field.
    center
        The tag for the center position field.
    fiber
        The tag for the fiber direction field.

    """

    cl: str
    center: str
    fiber: str
    normal: str


class MeshDef(TypedDict, total=True):
    """Definition of a mesh.

    Parameters
    ----------
    cylinder
        The definition of the cylinder mesh.

    """

    geo: GeoDef
    home: Path
    top: Mapping[_TOPS, TopSpec]
    fields: FieldTags
    bnds: Mapping[_BNDS, BndTag]
