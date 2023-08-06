from itertools import product


class BayesianNetworkx():

    # Clase representativo de una red bayesiana.
    # No toma parametros
    def __init__(self):
        self.nodes = []

    # Agrega los nodos a la red bayesiana.
    # Parametros: nombre del nodos, padres del nodo, tabla de probabilidad condicional
    def add_node(self, name, parents, cpt):
        node = {
            "name": name,
            "parents": parents,
            "cpt": cpt,
        }
        self.nodes.append(node)

    # Verifica que la red bayesiana este completamente descrita.
    # Verifica que cada probabilidad de las tablas sean iguales a 1, con una tolerancia de 0.01
    # Verifica que cada probabilidad de las tablas sean iguales a la probabilidad calculada, con una tolerancia de 0.01
    # No toma parametros
    def check_model(self):
        print("\n---RED COMPLETAMENTE DESCRITA---")
        for node in self.nodes:
            for cpt_entry in node["cpt"].values():
                if abs(cpt_entry[0] + cpt_entry[1] - 1) > 0.01:
                    return False

            for parent_states in node["cpt"].keys():
                parent_evidence = {
                    parent_name: parent_state for parent_name, parent_state in zip(node["parents"], parent_states)
                }
                cpt_prob = self.probability(node, parent_evidence)
                cpt_entry = node["cpt"][parent_states]
                if abs(cpt_entry[0] - cpt_prob[0]) > 0.01 or abs(cpt_entry[1] - cpt_prob[1]) > 0.01:
                    return False

        return True

    def print_all_cpts(self):
        print("\nForma Compacta:")
        print("+-----------------------+-----------------------+")
        print("| Nodo([Padres])        | CPT                   |")
        print("+-----------------------+-----------------------+")
        for node in self.nodes:
            cpt = node["cpt"]
            node_name = node["name"]
            parents = node["parents"]
            cpt_str = " | ".join("{}:{}".format(k, v) for k, v in cpt.items())
            print("| {} ({}) | {} |".format(node_name, parents, cpt_str))
            print("+-----------------------+-----------------------+")

    # Imprime la red bayesiana en forma compacta
    # No toma parametros
    def get_compact(self):
        print("\n---FORMA COMPACTA---")
        result2 = "P("
        result = ""
        for node in self.nodes:
            node_name = node["name"]
            result2 += node_name + ","
            parents = node["parents"]

            if not parents:
                result += f"P({node_name})"
            else:
                parents_str = ",".join(parents)
                result += f"P({node_name}|{parents_str})"

        result2 = result2[:-1] + ") = "
        result2 += result
        return result2

    # Imprime la red bayesiana en forma de factores
    # No toma parametros
    def get_factors(self):
        print("\n---FACTORES DE LA RED---")
        result = ""
        for node in self.nodes:
            cpt = node["cpt"]
            node_name = node["name"]
            parents = node["parents"]

            if not parents:
                result += f"P({node_name})\n"
            else:
                parents_str = ", ".join(parents)
                result += f"P({node_name}|{parents_str})\n"

            for parent_states, (phi_0, phi_1) in cpt.items():
                parent_states_str = ", ".join(str(s) for s in parent_states)
                result += f"  {parent_states_str}: {phi_0}, {phi_1}\n"

        return result

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
        print("| {}(0) | {:8.3f} |".format(variable, phi_0))
        print("+------+----------+")
        print("| {}(1) | {:8.3f} |".format(variable, phi_1))
        print("+------+----------+")

    def enumerate(self, variables, evidendce):
        if not variables:
            return 1

        Y = variables[0]
        if Y in evidendce:
            return self.probability(Y, evidendce[Y])[evidendce[Y]] * self.enumerate(variables[1:], evidendce)

        return self.probability(Y, 0)[0] * self.enumerate(variables[1:], evidendce) + self.probability(Y, 1)[1] * self.enumerate(variables[1:], evidendce)
