import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from typing import Protocol

class _FloatPairFn(Protocol):
    def __call__(self, x: float, r: float) -> float: ...

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

    def _dfdx(self, x, r, h=1e-8):
        return (self._f(x + h, r) - self._f(x - h, r)) / (2 * h)

    def find_bif(self):
        stable = []
        unstable = []
        x_edges = np.linspace(self._xmin, self._xmax, self._subs * 10, endpoint=True)
        for r in np.linspace(self._rmin, self._rmax, self._subs, endpoint=True):
            f_vals = np.array([self._f(x, r) for x in x_edges])
            for i in range(len(x_edges) - 1):
                if not (np.isfinite(f_vals[i]) and np.isfinite(f_vals[i + 1])):
                    continue
                if f_vals[i] * f_vals[i + 1] < 0:
                    try:
                        root = brentq(self._f, x_edges[i], x_edges[i + 1], args=(r,))
                        if self._dfdx(root, r) < 0:
                            stable.append((r, root))
                        else:
                            unstable.append((r, root))
                    except ValueError:
                        pass

        stable = np.array(stable)
        unstable = np.array(unstable)

        if stable.size > 0:
            plt.scatter(stable[:, 0], stable[:, 1], c='#FF8200', s=1, label='stable')
        if unstable.size > 0:
            plt.scatter(unstable[:, 0], unstable[:, 1], c='blue', s=1, label='unstable')

        plt.xlim(self._rmin, self._rmax)
        plt.ylim(self._xmin, self._xmax)
        plt.axhline(0, color='k', alpha=0.5)
        plt.axvline(0, color='k', alpha=0.5)
        plt.xlabel('r')
        plt.ylabel('x')
        plt.title(self._title if self._title else 'Bifurcation Diagram')
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
        self._save = True
        self._name = name