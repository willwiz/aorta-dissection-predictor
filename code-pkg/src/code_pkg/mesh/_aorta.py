from typing import TYPE_CHECKING, get_args

from ._types import MeshDefN, TopologyType

if TYPE_CHECKING:
    from pathlib import Path


def create_aorta_mesh_info(mesh_root: Path) -> MeshDefN[TopologyType]:
    return {
        "label": get_args(TopologyType),
        "geo": {"name": "full"},
        "home": mesh_root,
        "top": {
            "Disp": {"mesh": mesh_root / "Lin", "elem": "tet", "order": 1},
            "Pres": {"mesh": mesh_root / "Lin", "elem": "tet", "order": 1},
            "Inner": {"mesh": mesh_root / "Inner", "master": "Pres", "bnd": 3},
            "Outer": {"mesh": mesh_root / "Outer", "master": "Pres", "bnd": 1},
            "Inlet": {"mesh": mesh_root / "Inlet", "master": "Pres", "bnd": 2},
            "Outlet": {"mesh": mesh_root / "Outlet", "master": "Pres", "bnd": 4},
            "Brachial": {"mesh": mesh_root / "Brachial", "master": "Pres", "bnd": 7},
            "Carotid": {"mesh": mesh_root / "Carotid", "master": "Pres", "bnd": 6},
            "Subclavian": {"mesh": mesh_root / "Subclavian", "master": "Pres", "bnd": 5},
        },
        "bnds": {
            "Inlet": {"name": "Inlet", "tag": 2},
            "Outlet": {"name": "Outlet", "tag": 4},
            "Inner": {"name": "Inner", "tag": 3},
            "Outer": {"name": "Outer", "tag": 1},
            "Brachial": {"name": "Brachial", "tag": 7},
            "Carotid": {"name": "Carotid", "tag": 6},
            "Subclavian": {"name": "Subclavian", "tag": 5},
        },
        "fields": {
            "a_z": "Az-0.D",
            "a_c": "Ac-0.D",
            "a_r": "Ar-0.D",
            "Z": "Z-i.D",
            "C": "C-i.D",
            "R": "R-i.D",
        },
    }
