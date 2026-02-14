import numpy as np
import matplotlib.pyplot as plt
from typing import Protocol

class _FloatPairFn(Protocol):
    def __call__(self, x: tuple[float, float]) -> float: ...

class BifGraph:
    def __init__(self, function: _FloatPairFn):
        self._f =  function
        self._rmin   =  -10
        self._rmax   =   10
        self._xmin   =  -10
        self._xmax   =   10
        self._subs   = 1000
        self._result = None
        self._title  = None

    def _eval(self):
        r = np.linspace(self._rmin, self._rmax, self._subs, endpoint=True)
        x = np.flip(np.linspace(self._xmin, self._xmax, self._subs, endpoint=True))
        R, X = np.meshgrid(r, x, indexing='xy')

        grid = np.stack((R, X), axis=-1)

        self._result = np.apply_along_axis(self._f, axis=-1, arr=grid)

    def func(self, func: _FloatPairFn):
        self._f = func

    def title(self, title: str):
        self._title = title

    def rlim(self, tup: tuple[float, float]):
        self._rmin = tup[0]
        self._rmax = tup[1]

    def xlim(self, tup: tuple[float, float]):
        self._xmin = tup[0]
        self._xmax = tup[1]

    def subsections(self, num: int):
        self._subs = num
