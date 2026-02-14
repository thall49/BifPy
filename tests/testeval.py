from src.bifgraph import BifGraph
import numpy as np

def f(tup):
    return tup[0] - tup[1]

bg = BifGraph(f)

bg.xlim((-1, 1))
bg.rlim((-1, 1))
bg.subsections(5)

bg._eval()

print(bg._result)
print(bg._result.shape)