from pathlib import Path

from cheartpy.examples.arterial_universal_coordinate import uac_pfile
from code_pkg.data import setup_david_aorta
from code_pkg.mesh import create_aorta_mesh_info


def main() -> None:
    mesh = create_aorta_mesh_info(Path("mesh_david"))
    setup_david_aorta(mesh["top"]["Pres"]["mesh"]).unwrap()

    pfile = uac_pfile(
        top=mesh["top"]["Pres"],
        bc={
            "z": {
                mesh["bnds"]["Inlet"]["tag"]: 0.0,
                mesh["bnds"]["Outlet"]["tag"]: 1.0,
                mesh["bnds"]["Brachial"]["tag"]: 0.44,
                mesh["bnds"]["Carotid"]["tag"]: 0.45,
                mesh["bnds"]["Subclavian"]["tag"]: 0.46,
            },
            "r": {mesh["bnds"]["Inner"]["tag"]: 0.0, mesh["bnds"]["Outer"]["tag"]: 1.0},
        },
    )
    with Path("test.P").open("w") as f:
        pfile.write(f)


if __name__ == "__main__":
    main()
