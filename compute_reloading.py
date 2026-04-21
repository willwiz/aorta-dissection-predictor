from pathlib import Path

from cheartpy.io import chread_d, chwrite_d_utf
from cheartpy.search import get_var_index
from pytools.result import Err, Ok


def main() -> None:
    home = Path("results_aorta_forward")
    disps = [f.name for f in home.glob("U-*.D")]
    match get_var_index(disps, "U"):
        case Ok(index): ...  # fmt: skip
        case Err(err):
            print(f"Error: {err}")
            raise SystemExit(1)
    u_list = [chread_d(home / f"U-{i}.D") for i in index]
    total_u = -chread_d(home / "U-100.D")
    forward_u = [total_u + u for u in reversed(u_list)]
    Path("prestretch_data").mkdir(exist_ok=True)
    for i, u in enumerate(forward_u):
        chwrite_d_utf(Path("prestretch_data") / f"Disp-{i}.D", u)


if __name__ == "__main__":
    main()
