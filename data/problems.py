# /// script
# dependencies = []
# ///

from pathlib import Path
from typing import TYPE_CHECKING

from .mesh import PILOT_CYLINDER

if TYPE_CHECKING:
    from collections.abc import Sequence

    from code_pkg.components import ProblemDef


MAIN_PROBLEMS: dict[str, Sequence[ProblemDef]] = {
    "forward": [
        {
            "time": {"end": 200, "step": 1},
            "mesh": PILOT_CYLINDER,
            "mode": "forward",
            "models": [{"matlaw": "NeoHookean", "k": 100.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 100.0, "duration": 50},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "output_dir": Path(f"results_forward_{t}"),
        }
        for t in ["old", "new"]
    ],
    "inverse": [
        {
            "time": {"end": 200, "step": 1},
            "mesh": PILOT_CYLINDER,
            "mode": "inverse",
            "models": [{"matlaw": "NeoHookean", "k": 100.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 100.0, "duration": 50},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "output_dir": Path(f"results_inverse_{t}"),
        }
        for t in ["i", "t"]
    ],
    "corrected": [
        {
            "time": {"end": 200, "step": 1},
            "mesh": PILOT_CYLINDER,
            "mode": "inverse",
            "models": [{"matlaw": "NeoHookean", "k": 100.0}],
            "bc": {
                "Pres": {"mode": "linear", "amp": 100.0, "duration": 50},
                "Inlet": "SLIP",
                "Outlet": "HOLD",
            },
            "output_dir": Path(f"results_correct_{t}"),
        }
        for t in ["i", "t"]
    ],
}
