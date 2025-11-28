from numba import complex128, float64
from numba.pycc import CC
from numba.types import UniTuple

import pyquartic_numba


def build_numba_extensions():
    cc = CC("pyquartic")
    cc.verbose = True

    cc.export("solve_cubic", UniTuple(complex128, 3)(float64, float64, float64, float64))(pyquartic_numba.solve_cubic)
    cc.export("solve_cubic_one", float64(float64, float64, float64))(pyquartic_numba.solve_cubic_one)
    cc.export("solve_quartic", UniTuple(complex128, 4)(float64, float64, float64, float64, float64))(pyquartic_numba.solve_quartic)
    cc.compile()

if __name__ == "__main__":
    build_numba_extensions()
