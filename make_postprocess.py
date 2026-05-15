from pathlib import Path

from cheartpy.io import chread_d, chwrite_d_utf


def main(mesh: Path, root: Path) -> None:
    zrc = chread_d(root / "RZC-100.D").reshape(-1, 3, 3)
    chwrite_d_utf(mesh / "R-t.D", zrc[:, 0, :])
    chwrite_d_utf(mesh / "Z-t.D", zrc[:, 1, :])
    chwrite_d_utf(mesh / "C-t.D", zrc[:, 2, :])


if __name__ == "__main__":
    main(Path("mesh_aorta"), Path("results_aorta_inverse"))
    main(Path("mesh_circ"), Path("results_circ_inverse"))
    main(Path("mesh_plane"), Path("results_plane_inverse"))
