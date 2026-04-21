# /// script
# dependencies = ["data/problems.py"]
# ///

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from cheartpy.io.api import chread_d, chwrite_d_utf

if TYPE_CHECKING:
    from pytools.arrays import A2


def normalize_by_row[F: np.floating](vals: A2[F]) -> A2[F]:
    norm = np.sqrt(np.einsum("...i,...i", vals, vals))
    # norm[norm < _DBL_TOL] = 1.0
    return vals / norm[:, np.newaxis]


def main() -> None:
    mesh = Path("mesh_mia")
    c = chread_d(mesh / "C-0.D")
    r = chread_d(mesh / "R-0.D")
    z = chread_d(mesh / "Z-0.D")
    f = chread_d(Path() / "results_release_mia_forward" / "F-100.D")
    f = f.reshape((-1, 3, 3))
    # f_invt = np.einsum("ijk->ikj", np.linalg.inv(f))
    # f_invt = np.linalg.inv(f)
    new_c = normalize_by_row(np.einsum("ijk,ik->ij", f, c))
    new_r = normalize_by_row(np.einsum("ijk,ik->ij", f, r))
    new_z = normalize_by_row(np.einsum("ijk,ik->ij", f, z))
    c_res = new_c - c
    r_res = new_r - r
    z_res = new_z - z
    c_norm = np.sqrt(np.einsum("ij,ij->i", c, c))
    r_norm = np.sqrt(np.einsum("ij,ij->i", r, r))
    z_norm = np.sqrt(np.einsum("ij,ij->i", z, z))
    print(c_norm.max())
    print(r_norm.max())
    print(z_norm.max())
    print(c_norm.min())
    print(r_norm.min())
    print(z_norm.min())
    c_norm = np.sqrt(np.einsum("ij,ij->i", new_c, new_c))
    r_norm = np.sqrt(np.einsum("ij,ij->i", new_r, new_r))
    z_norm = np.sqrt(np.einsum("ij,ij->i", new_z, new_z))
    print(c_norm.max())
    print(r_norm.max())
    print(z_norm.max())
    print(c_norm.min())
    print(r_norm.min())
    print(z_norm.min())
    print(np.abs(c_res).max())
    print(np.abs(r_res).max())
    print(np.abs(z_res).max())
    # chwrite_d_utf(Path() / "mesh_bent_cylinder" / "Ct-0.D", new_c)
    # chwrite_d_utf(Path() / "mesh_bent_cylinder" / "Rt-0.D", new_r)
    # chwrite_d_utf(Path() / "mesh_bent_cylinder" / "Zt-0.D", new_z)
    chwrite_d_utf(mesh / "C-t.D", new_c)
    chwrite_d_utf(mesh / "R-t.D", new_r)
    chwrite_d_utf(mesh / "Z-t.D", new_z)


if __name__ == "__main__":
    main()
