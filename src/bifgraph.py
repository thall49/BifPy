import numpy as np
import matplotlib.pyplot as plt
from typing import Protocol

class _FloatPairFn(Protocol):
    def __call__(self, x: tuple[float, float]) -> float: ...

class BifGraph:
    def __init__(self, function: _FloatPairFn):
        self._f = function
        self._rmin =   -10
        self._rmax =    10
        self._xmin =   -10
        self._xmax =    10
        self._subs =  1000
        self._grid =  None

    def _gen_grid(self):
        r = np.linspace(self._rmin, self._rmax, self._subs, endpoint=True)
        x = np.linspace(self._xmin, self._xmax, self._subs, endpoint=True)

        X, Y = np.meshgrid(r, x, indexing='xy')


        self._grid = np.stack((X, Y), axis=1)