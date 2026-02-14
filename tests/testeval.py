import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.bifgraph import BifGraph

def f(x, r):
    return 

bg = BifGraph(f)

bg.find_bif()
