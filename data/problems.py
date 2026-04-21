# /// script
# dependencies = []
# ///

from pathlib import Path
from typing import TYPE_CHECKING, Literal

from .mesh import NEW_CYLINDER

if TYPE_CHECKING:
    from collections.abc import Sequence

    from code_pkg.components import ProblemDef

_RESULTS_ROOT = Path("results")
_TOPS = Literal["Disp", "Pres", "Inlet", "Outlet", "Inner", "Outer"]
RELEASE_PROBLEM: ProblemDef = {
    "name": "release",
    "time": {"end": 300, "step": 0.01},
    "mesh": NEW_CYLINDER,
    "mode": "forward",
    "models": [{"matlaw": "NeoHookean", "k": 10.0}],
    "bc": {
        "Pres": {"mode": "linear", "amp": 2.1, "duration": 1.0},
        "Inlet": "SLIP",
        "Outlet": "HOLD",
    },
    "res_strain": {"mode": "tensor", "strain": 0.2},
    "output_dir": Path("results_release"),
}

MAIN_PROBLEMS: dict[str, Sequence[ProblemDef]] = {
    "forward": [
        {
            "name": "forward_old",
            "time": {"end": 200, "step": 0.01},
            "mesh": NEW_CYLINDER,
            "mode": "forward",
            "models": [{"matlaw": "NeoHookean", "k": 10.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 2.1, "duration": 1.0},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "res_strain": {"mode": "tensor", "strain": 0.2},
            "output_dir": _RESULTS_ROOT,
        },
    ],
    "inverse": [
        {
            "name": "inverse_old_reference",
            "time": {"end": 200, "step": 0.01},
            "mesh": NEW_CYLINDER,
            "mode": "inverse",
            "models": [{"matlaw": "NeoHookean", "k": 10.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 2.1, "duration": 1.0},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "res_strain": {"mode": "tensor", "strain": 0.2},
            "output_dir": _RESULTS_ROOT,
        },
        {
            "name": "inverse_old_deformed",
            "time": {"end": 200, "step": 0.01},
            "mesh": NEW_CYLINDER,
            "mode": "inverse",
            "models": [{"matlaw": "NeoHookean", "k": 10.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 2.1, "duration": 1.0},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "res_strain": {"mode": "tensor", "strain": 0.2},
            "output_dir": _RESULTS_ROOT,
        },
        {
            "name": "inverse_new_reference",
            "time": {"end": 200, "step": 0.01},
            "mesh": NEW_CYLINDER,
            "mode": "inverse",
            "models": [{"matlaw": "NeoHookean", "k": 10.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 2.1, "duration": 1.0},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "res_strain": {"mode": "vector", "strain": 0.2},
            "output_dir": _RESULTS_ROOT,
        },
        {
            "name": "inverse_new_deformed",
            "time": {"end": 200, "step": 0.01},
            "mesh": NEW_CYLINDER,
            "mode": "inverse",
            "models": [{"matlaw": "NeoHookean", "k": 10.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 2.1, "duration": 1.0},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "res_strain": {"mode": "deformed-vector", "strain": 0.2},
            "output_dir": _RESULTS_ROOT,
        },
    ],
}


PILOT_PROBLEMS: dict[str, Sequence[ProblemDef]] = {
    "forward": [
        {
            "name": f"forward_{t}",
            "time": {"end": 200, "step": 0.01},
            "mesh": NEW_CYLINDER,
            "mode": "forward",
            "models": [{"matlaw": "NeoHookean", "k": 100.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 2.1, "duration": 1.0},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "output_dir": Path(f"results_forward_{t}"),
        }
        for t in ["old", "new"]
    ],
    "inverse": [
        {
            "name": f"inverse_{t}",
            "time": {"end": 200, "step": 0.01},
            "mesh": NEW_CYLINDER,
            "mode": "inverse",
            "models": [{"matlaw": "NeoHookean", "k": 100.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 2.1, "duration": 1.0},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "output_dir": Path(f"results_inverse_{t}"),
        }
        for t in ["i", "t"]
    ],
    "corrected": [
        {
            "name": f"corrected_{t}",
            "time": {"end": 200, "step": 0.01},
            "mesh": NEW_CYLINDER,
            "mode": "inverse",
            "models": [{"matlaw": "NeoHookean", "k": 100.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 2.1, "duration": 1.0},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "output_dir": Path(f"results_correct_{t}"),
        }
        for t in ["i", "t"]
    ],
}
