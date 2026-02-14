import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from typing import Protocol

class _FloatPairFn(Protocol):
    def __call__(self, x: tuple[float, float]) -> float: ...

class BifGraph:
    def __init__(self, function: _FloatPairFn):
        self._f =   function
        self._rmin   =   -10
        self._rmax   =    10
        self._xmin   =   -10
        self._xmax   =    10
        self._subs   =  1000
        self._result =  None
        self._grid   =  None
        self._title  =  None
        self._save   = False
        self._name   =  None

    def find_bif(self):
        pos_roots = []
        neg_roots = []
        for r in np.linspace(self._rmin, self._rmax, self._subs, endpoint=True):
            try:
                x_pos = brentq(self._f, 0, self._xmax, args=(r,))
                pos_roots.append((r, x_pos))
            except ValueError:
                pass

            try:
                x_neg = brentq(self._f, self._xmin, 0, args=(r,))
                neg_roots.append((r, x_neg))
            except ValueError:
                pass
        
        pos_roots = np.array(pos_roots)
        neg_roots = np.array(neg_roots)

        plt.plot(pos_roots[:, 0], pos_roots[:, 1], 'r', label='pos')
        plt.plot(neg_roots[:, 0], neg_roots[:, 1], 'b', label='neg')

        plt.axvline(0, color='k', linestyle='--', alpha=0.5)
        plt.xlabel('r')
        plt.ylabel('x')
        plt.title('Test')
        plt.legend()
        plt.show()


    def _eval(self):
        r = np.linspace(self._rmin, self._rmax, self._subs, endpoint=True)
        x = np.flip(np.linspace(self._xmin, self._xmax, self._subs, endpoint=True))
        R, X = np.meshgrid(r, x, indexing='xy')

        self._grid = np.stack((R, X), axis=-1)

        self._result = np.apply_along_axis(self._f, axis=-1, arr=self._grid)

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

    def name(self, name: str):
        self._show = True
        self._name = name