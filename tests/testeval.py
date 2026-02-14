from src.bifgraph import BifGraph
import numpy as np

def f(r, x):
    return x**2 - r

bg = BifGraph(f)

bg.find_bif()