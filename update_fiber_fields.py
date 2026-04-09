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


def main(mesh: Path) -> None:
    r = chread_d(mesh / "transmural.D")
    z = chread_d(mesh / "longitudinal.D")
    z = z - (np.einsum("ij,ij->i", z, r) / np.einsum("ij,ij->i", r, r))[:, np.newaxis] * r
    c = np.cross(r, z)
    c = normalize_by_row(c)
    r = normalize_by_row(r)
    z = normalize_by_row(z)
    cxc = np.einsum("ij,ik->ijk", c, c)
    rxr = np.einsum("ij,ik->ijk", r, r)
    zxz = np.einsum("ij,ik->ijk", z, z)
    chwrite_d_utf(mesh / "CxC-0.D", cxc.reshape(cxc.shape[0], 9))
    chwrite_d_utf(mesh / "RxR-0.D", rxr.reshape(rxr.shape[0], 9))
    chwrite_d_utf(mesh / "ZxZ-0.D", zxz.reshape(zxz.shape[0], 9))
    chwrite_d_utf(mesh / "res-0.D", (cxc + rxr + zxz).reshape(cxc.shape[0], 9))
    c_norm = np.sqrt(np.einsum("ij,ij->i", c, c))
    r_norm = np.sqrt(np.einsum("ij,ij->i", r, r))
    z_norm = np.sqrt(np.einsum("ij,ij->i", z, z))
    cr = np.einsum("ij,ij->i", c, r)
    cz = np.einsum("ij,ij->i", c, z)
    rz = np.einsum("ij,ij->i", r, z)
    print(cr.min())
    print(cr.max())
    print(cz.min())
    print(cz.max())
    print(rz.min())
    print(rz.max())
    print(c_norm.min())
    print(c_norm.max())
    print(r_norm.min())
    print(r_norm.max())
    print(z_norm.min())
    print(z_norm.max())
    chwrite_d_utf(mesh / "C-0.D", c)
    chwrite_d_utf(mesh / "R-0.D", r)
    chwrite_d_utf(mesh / "Z-0.D", z)


if __name__ == "__main__":
    main(Path("mesh_mia"))
