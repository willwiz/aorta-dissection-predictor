import importlib.resources
from typing import TYPE_CHECKING

from cheartpy.fe.aliases import VolumeTopologyDef
from cheartpy.mesh import import_cheart_mesh
from pytools.result import Err, Ok, Result

if TYPE_CHECKING:
    from pathlib import Path


def setup_david_aorta(name: Path) -> Result[VolumeTopologyDef]:
    with importlib.resources.path("code_pkg.data", "david_aorta", "model") as template_path:
        match import_cheart_mesh(template_path):
            case Ok(mesh):
                name.parent.mkdir(parents=True, exist_ok=True)
                mesh.save(name)
            case Err(err):
                return Err(err)
    return Ok(VolumeTopologyDef(elem="tet", order=1, mesh=name))
