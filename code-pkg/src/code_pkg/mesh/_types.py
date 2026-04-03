from pathlib import Path
from typing import Literal, Required

from pytools.arrays import ToFloat, ToInt
from typing_extensions import TypedDict


class CylinderDef(TypedDict, total=False):
    """Definition of a cylinder mesh.

    Parameters
    ----------
    size
        The number of elements in each direction (r, q, z).
    shape
        The physical dimensions of the cylinder (rin, rout, length).
    offset
        The offset of the inner surface from the centerline, as a fraction of the wall thickness. Default is 0.0 (left aligned).
    orientation
        The axis along which the cylinder is oriented. Must be one of "x", "y", or "z". Default is "z".
    """

    size: Required[tuple[ToInt, ToInt, ToInt]]
    shape: Required[tuple[ToFloat, ToFloat, ToFloat]]
    offset: ToFloat
    orientation: Literal["x", "y", "z"]
    warp: bool


type GeoDef = CylinderDef
type ElementTypes = Literal["HEX", "TET"]
_TOPS = Literal["Disp", "Pres"]
_FIELDS = Literal["cl", "center", "fiber"]


class BndTags(TypedDict, total=True):
    """Definition of boundary condition tags.

    Parameters
    ----------
    inlet
        The tag for the inlet boundary condition.
    outlet
        The tag for the outlet boundary condition.
    wall
        The tag for the wall boundary condition.
    """

    inlet: str
    outlet: str
    inner: str
    outer: str


class TopTags(TypedDict, total=True):
    """Definition of top tags.

    Parameters
    ----------
    disp
        The tag for the displacement field.
    pres
        The tag for the pressure field.
    """

    disp: str
    pres: str


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
    elem: ElementTypes
    order: int
    top: TopTags
    fields: FieldTags
    bnds: BndTags
