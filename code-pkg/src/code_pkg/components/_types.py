from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal, LiteralString, NamedTuple, Required, TypedDict

if TYPE_CHECKING:
    from collections.abc import Mapping, ValuesView
    from pathlib import Path

    from cheartpy.fe.trait import ICheartTopology, ITopInterface, IVariable

    from code_pkg.mesh import MeshDef

type TopologyType = Literal["Disp", "Pres", "Inlet", "Outlet", "Inner", "Outer"]


class TopologyMap[M: LiteralString]:
    _tops: Mapping[M, ICheartTopology]
    _ifaces: Mapping[int, ITopInterface]

    def __init__(self, *iface: ITopInterface, kwargs: Mapping[M, ICheartTopology]) -> None:
        self._ifaces = {hash(i): i for i in iface}
        self._tops = kwargs

    def __getitem__(self, key: M, /) -> ICheartTopology:
        return self._tops[key]

    @property
    def ifaces(self) -> ValuesView[ITopInterface]:
        return self._ifaces.values()


class LinearPressure(TypedDict, total=True):
    mode: Literal["linear"]
    amp: float
    duration: float


type PressureDef = LinearPressure


class BCDef(TypedDict, total=False):
    Pres: Required[PressureDef]
    Inlet: Literal["SLIP", "HOLD"]
    Outlet: Literal["SLIP", "HOLD"]


class TimeDef(TypedDict, total=False):
    start: int
    end: Required[int]
    step: Required[int]


class NeoHookeanDef(TypedDict, total=True):
    matlaw: Literal["NeoHookean"]
    k: float


type ModelDef = NeoHookeanDef


class ProblemDef(TypedDict, total=False):
    time: Required[TimeDef]
    mesh: Required[MeshDef]
    mode: Literal["forward", "inverse"]
    models: Required[Sequence[ModelDef]]
    bc: Required[BCDef]
    output_dir: Path


class Variables(NamedTuple):
    Xi: IVariable
    Xt: IVariable
    U: IVariable
    P: IVariable
