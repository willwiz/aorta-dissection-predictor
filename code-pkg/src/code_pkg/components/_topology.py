from typing import TYPE_CHECKING

from cheartpy.fe.api import (
    create_topologies,
)

from ._types import TopologyMap

if TYPE_CHECKING:
    from code_pkg.mesh import MeshDefN


def create_prob_topologies[T](mesh: MeshDefN[T]) -> TopologyMap[T]:
    tops, ifaces = create_topologies(mesh["top"])
    return TopologyMap[T](*ifaces, kwargs=tops)
