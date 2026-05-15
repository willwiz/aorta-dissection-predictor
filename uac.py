import uuid
from pathlib import Path

from cheartpy.cmd_tools.cli import run_prep
from cheartpy.examples.arterial_universal_coordinate import uac_pfile
from code_pkg.data import setup_david_aorta
from code_pkg.mesh import create_aorta_mesh_info


def main() -> None:
    mesh = create_aorta_mesh_info(Path("mesh_david"))
    setup_david_aorta(mesh["top"]["Pres"]["mesh"]).unwrap()
    problem_name = f"{uuid.uuid7}.P"
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
        output_dir=mesh["home"],
    )
    with Path(problem_name).open("w") as f:
        pfile.write(f)
    run_prep(problem_name)


if __name__ == "__main__":
    main()
