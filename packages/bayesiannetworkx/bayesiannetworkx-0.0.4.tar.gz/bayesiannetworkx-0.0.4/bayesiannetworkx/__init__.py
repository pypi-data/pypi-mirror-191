class BayesianNetworkx():
    def __init__(self):
        self.nodes = []

    def add_node(self, name, parents, cpt):
        node = {
            "name": name,
            "parents": parents,
            "cpt": cpt
        }
        self.nodes.append(node)

    def joint_probability(self, evidence):
        joint_prob = 1
        for node in self.nodes:
            if node["name"] in evidence:
                joint_prob *= self.probability(node, evidence)
        return joint_prob

    def probability(self, node, evidence=None):
        if evidence is None:
            evidence = {}

        index = tuple(evidence[parent_name]
                      for parent_name in node["parents"])
        phi_0 = node["cpt"][index][0]
        phi_1 = node["cpt"][index][1]
        return (phi_0, phi_1)

    def printProbability(self, variable, evidence={}):
        node = next(n for n in self.nodes if n["name"] == variable)
        phi_0, phi_1 = self.probability(node, evidence)
        print("+------+----------+")
        print("| {}    |   phi({}) |".format(variable, variable))
        print("+======+==========+")
        print("| {}(0) | {:8.4f} |".format(variable, phi_0))
        print("+------+----------+")
        print("| {}(1) | {:8.4f} |".format(variable, phi_1))
        print("+------+----------+")
