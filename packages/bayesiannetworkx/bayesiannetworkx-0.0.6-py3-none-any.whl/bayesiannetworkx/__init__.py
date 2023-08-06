from collections import defaultdict
from prettytable import PrettyTable, ALL


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
        result = []
        for node in self.nodes:
            cpt = node["cpt"]
            node_name = node["name"]
            parents = node["parents"]

            if not parents:
                result.append(("P(" + node_name + ")", "", "", ""))
                for parent_states, (phi_0, phi_1) in cpt.items():
                    result.append(("", node_name + "(0)", phi_0, ""))
                    result.append(("", node_name + "(1)", phi_1, ""))
                    result.append(("", "", "", ""))
            else:
                result.append(
                    ("P(" + node_name + "|" + ", ".join(parents) + ")", "", "", ""))
                for parent_states, (phi_0, phi_1) in cpt.items():
                    parent_states_str = ", ".join(
                        str(s) for s in parent_states)
                    result.append(("", parent_states_str, phi_0, phi_1))

        return result

    def print_factors(self, factors):
        print("\n---FACTORES DE LA RED---")
        table = PrettyTable()
        table.field_names = ["var", "phi(var)", "P(0)", "P(1)"]
        table.hrules = ALL
        for factor in factors:
            table.add_row(factor)
        print(table)

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

    # funcion para imprimir la probabilidad de una variable dada evidencia
    def print_result(self, variable, evidence={}):
        print("\n---INFERENCIA EXACTA---")
        header = "+------+----------+"
        print(header)
        print("| {}    |   phi({}) |".format(variable, variable))
        print("+======+==========+")
        for key in [0, 1]:
            result = self.enumeration_ask(variable, evidence)
            print("| {}({}) | {:8.3f} |".format(variable, key, result[key]))
            print(header)

    def getProbability(self, variable, value, evidence={}):
        node = next(n for n in self.nodes if n["name"] == variable)
        phi_0, phi_1 = self.probability(node, evidence)
        if value == 0:
            return phi_0
        elif value == 1:
            return phi_1

    # Funcion que calcula la probabilidad de una variable dada evidencia
    # Parametros: variable: una lista de variables, evidencia: un diccionario con variables y sus valores

    def enumeration_ask(self, X, evidence):

        Q = defaultdict(float)
        X_node = next(n for n in self.nodes if n["name"] == X)
        for xi in [0, 1]:
            evidence[X] = xi
            Q[xi] = self.enumerate_all(self.nodes, evidence)
        return self.normalize(Q)

    # funcion recursuva para obtener la inferencia exacta usando el algoritmo de enumeracion
    def enumerate_all(self, nodes, evidence):

        if not nodes:
            return 1.0
        Y = nodes[0]
        Y_name = Y["name"]
        if Y_name in evidence:
            return Y["cpt"][tuple(evidence[parent_name] for parent_name in Y["parents"])][evidence[Y_name]] * self.enumerate_all(nodes[1:], evidence)
        else:
            sum = 0
            for yi in [0, 1]:
                evidence[Y_name] = yi
                sum += Y["cpt"][tuple(evidence[parent_name] for parent_name in Y["parents"])
                                ][yi] * self.enumerate_all(nodes[1:], evidence)
            del evidence[Y_name]
            return sum

    def normalize(self, Q):

        total = sum(Q.values())
        for x in Q:
            Q[x] /= total
        return Q
