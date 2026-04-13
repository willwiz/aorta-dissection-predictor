import numpy as np
from cheartpy.io import chwrite_time_utf


def main() -> None:
    dt = np.concatenate((np.full(99, 0.01), np.full(1, 0.02), np.full(100, 0.03)))
    chwrite_time_utf("time.step", dt)


if __name__ == "__main__":
    main()
