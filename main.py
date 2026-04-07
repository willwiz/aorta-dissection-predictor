import argparse
from logging import config
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from cheartpy.cmd_tools.cli import CheartErrorCode, run_prep, run_problem
from cheartpy.io.api import chread_d, chwrite_d_utf
from code_pkg import main_pfile
from pydantic import BaseModel
from pytools.parallel import ThreadedRunner

from data.problems import MAIN_PROBLEMS

if TYPE_CHECKING:
    from code_pkg.components import ProblemDef
    from pytools.arrays import A2
_QUAD_ORDER = 2

parser = argparse.ArgumentParser("main")
parser.add_argument("--overwrite", action="store_true")
parser.add_argument("--cores", "-n", type=int, default=8)
parser.add_argument("--parallel", type=int, default=1)
parser.add_argument("--dry-run", action="store_true")


class Config(BaseModel):
    overwrite: bool
    cores: int
    parallel: int
    dry_run: bool


def parse_cmdline_args(args: list[str] | None = None) -> Config:
    return Config(**vars(parser.parse_args(args)))

def normalize_by_row[F: np.floating](vals: A2[F]) -> A2[F]:
    norm = np.sqrt(np.einsum("...i,...i", vals, vals))
    return vals / norm[:, np.newaxis]


def update_deformed_mesh(prob: ProblemDef) -> None:
    if prob.get("mode") != "forward":
        return
    mesh = prob["mesh"]
    output_dir = prob.get("output_dir") or Path.cwd()
    c = chread_d(mesh["home"] / "C-0.D")
    r = chread_d(mesh["home"] / "R-0.D")
    z = chread_d(mesh["home"] / "Z-0.D")
    u = chread_d(output_dir / prob["name"] / "U-200.D")
    x = chread_d(output_dir / prob["name"] / "Xi-0.D")
    f = chread_d(output_dir / prob["name"] / "DeformationGradient-200.D")
    f = f.reshape((-1, 3, 3))
    new_c = normalize_by_row(np.einsum("ijk,ik->ij", f, c))
    new_r = normalize_by_row(np.einsum("ijk,ik->ij", f, r))
    new_z = normalize_by_row(np.einsum("ijk,ik->ij", f, z))
    new_x = x + u
    chwrite_d_utf(mesh["home"] / "C-t.D", new_c)
    chwrite_d_utf(mesh["home"] / "R-t.D", new_r)
    chwrite_d_utf(mesh["home"] / "Z-t.D", new_z)
    chwrite_d_utf(mesh["home"] / "X-t.D", new_x)


def is_complete(prob: ProblemDef, config: Config) -> bool:
    if config.overwrite:
        return False
    output_dir = prob.get("output_dir") or Path.cwd()
    return (output_dir / prob["name"] / "U-200.D").exists()

def report_completion(prob: ProblemDef, err: int) -> str:
    if err == 0:
        return f"{prob['name']}: complete successfully."
    code_msg = (
        f"{CheartErrorCode(err)}"
        if err in CheartErrorCode._value2member_map_
        else f"{CheartErrorCode.UNKNOWN} = {err}"
    )
    return f"{prob['name']}: failed with error {code_msg}"

def run_pfile(prob: ProblemDef, config: Config) -> str:
    if is_complete(prob, config):
        return f"{prob['name']}: already complete"
    pfile = main_pfile(prob)
    output_dir = prob.get("output_dir") or Path.cwd()
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    file = (output_dir / prob["name"]).with_suffix(".P")
    with file.open("w") as f:
        pfile.write(f)
    if config.dry_run:
        return f"{prob['name']}: dry run, not executing"
    if not (prob["mesh"]["home"] / (prob["mesh"]["top"]["Disp"]["prefix"] + "_FE.PART")).exists():
        run_prep(file)
    err = run_problem(file, log=True, verbosity="PEDANTIC", cores=config.cores)
    update_deformed_mesh(prob)
    return report_completion(prob, err)


if __name__ == "__main__":
    config = parse_cmdline_args()
    with ThreadedRunner(thread=config.parallel) as runner:
        for p in MAIN_PROBLEMS["forward"]:
            runner.submit(run_pfile, p, config)
    with ThreadedRunner(thread=config.parallel) as runner:
        for p in MAIN_PROBLEMS["inverse"]:
            runner.submit(run_pfile, p, config)
