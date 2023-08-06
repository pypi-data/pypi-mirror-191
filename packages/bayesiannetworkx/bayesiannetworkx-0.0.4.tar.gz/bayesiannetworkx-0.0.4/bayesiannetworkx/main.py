import __init__ as BayesianNetworkx
from __init__ import *

bn = BayesianNetworkx()

bn.add_node("A", [], {(): (0.1, 0.9)})
bn.add_node("B", ["A"], {(0,): (0.4, 0.6), (1,): (0.7, 0.3)})
bn.add_node("C", ["A"], {(0,): (0.8, 0.2), (1,): (0.2, 0.8)})

evidence = {"A": 1, "B": 0}

bn.printProbability("C", evidence)
