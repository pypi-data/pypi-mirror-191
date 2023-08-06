# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bayesiannetworkx']

package_data = \
{'': ['*']}

install_requires = \
['python-semantic-release>=7.33.1,<8.0.0', 'semver>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'bayesiannetworkx',
    'version': '0.0.5',
    'description': '',
    'long_description': '# Inteligencia Artificial: Laboratorio 2 - Inferencia Probabilistica\n\n## Descripcion \nLa clase BayesianNetworkx representa una red bayesiana, un modelo probabilístico que se utiliza en el aprendizaje automático para representar la dependencia entre variables. La clase tiene métodos para agregar nodos a la red, comprobar que la red esté completamente descrita, imprimir la red en forma compacta y en forma de factores, y calcular la probabilidad de un nodo dado un conjunto de evidencia.\n\n- `add_node()`: permite agregar nodos a la red, especificando el nombre del nodo, los padres del nodo y la tabla de probabilidad condicional. \n\n- `check_model()`: verifica que cada probabilidad en las tablas de probabilidad condicional sumen 1 y que las probabilidades calcuadas sean iguales a las de la tabla con una tolerancia de 0.01. Retorna un booleano:\n```python\nTrue\n```\n\n- `get_compact()`: imprime la representacio de la red bayesiana en forma compacta. Retorna un string de la siguiente manera:\n```python\nP(R,T,A,J,M) = P(R)P(T)P(A|R,T)P(J|A)P(M|A)\n```\n\n- `get_factors`: Imprime todos los factores de la red bayesiana. Retorna un string de la siguiente manera:\n```python\nP(R)\n  : 0.999, 0.001\nP(T)\n  : 0.998, 0.002\nP(A|R, T)\n  0, 0: 0.999, 0.001\n  0, 1: 0.71, 0.29\n  1, 0: 0.06, 0.94\n  1, 1: 0.05, 0.95\nP(J|A)\n  0: 0.95, 0.05\n  1: 0.1, 0.9\nP(M|A)\n  0: 0.99, 0.01\n  1: 0.3, 0.7\n```\n\n- `enumarate(variables, evidence)`: Imprime la probabilidad de distribucion de una variable, dado evidencia de otras variables de la red. El parametro de variables, es una lista de las variables de quines obtener los resultados. Y el parametro evidence es un diccionario que contiene los valores de las variables dadas. Ejemplo: `bn.enumarate(["R"], {"J": 1, "M": 1})` Retorna un string de la siguiente manera:\n```python\n+------+----------+\n| A    |   phi(A) |\n+======+==========+\n| A(0) |    0.050 |\n+------+----------+\n| A(1) |    0.950 |\n+------+----------+\n```\n\n## Uso\n1. Se debe de importar la libreria bayesiannetworkx.\n```python\nimport bayesiannetworkx as bnx\n```\n\n2. Para crear una instancia de la red, no se necesita ningun parametro.\n```python\nbn = bnx.BayesianNetworkx()\n```\n\n3. La red se arma a la hora de crear los nodos y agregarlos a la red. Un nodo consiste de un nombre, una lista de padres, y un diccionario con la tabla de probabilidades. Un nodo tiene que seguir el siguiente formato:\n```python\nnode = {\n            "name": name,\n            "parents": parents,\n            "cpt": cpt,\n        }\n```\n\nCreando y agregando un nodo sin padres.\n```python\nbn.add_node("R", [], {(): [0.999, 0.001]})\n```\nCreando y agregando un nodo con padres. \n\n```python\nbn.add_node("A", ["R", "T"], {(0, 0): [0.999, 0.001], (0, 1): [0.71, 0.29], (1, 0): [0.06, 0.94], (1, 1): [0.05, 0.95]})\n```\n\n4. Finalmente, la red esta creada, y se puede utilizar cualquiera de las funciones mencionadas anteriormente para poder obtener la informacion y probabilidades de la red bayesiana. \n\n## Ejemplo\nEl siguiente codigo muestra el clasico ejemplo de la alarma. Para este ejemplo debemos de considerar un par de cosas. \n- Tenemos una alarma antirrobo instalada en una casa.\n    -  La alarma salta normalmente con la presencia de ladrones.\n    - Pero tambien cuando ocurren temblores de tierra.\n- Tenemos dos vecinos en la casa, Juan y Maria, que han prometido llamar a la policia si oyen la alarma.\n    - Juan y Mara podrian no llamar aunque la alarma sonara: por tener musica muy alta en su casa, por ejemplo.\n    - Incluso podran llamar aunque no hubiera sonado: por confundirla con un telefono, por ejemplo.\n\n Con esta informacion, ya podemos armar la red bayesiana. Siendo "R" el nodo del robo, "T" el nodo del temblor, "A" el nodo de la alarma, "J" el nodo de Juan y "M" el nodo de Maria. \n ```python\nimport bayesiannetworkx as bnx\n\nbn = bnx.BayesianNetworkx()\n\nbn.add_node("R", [], {(): [0.999, 0.001]})\nbn.add_node("T", [], {(): [0.998, 0.002]})\nbn.add_node("A", ["R", "T"], {(0, 0): [0.999, 0.001], (0, 1): [0.71, 0.29], (1, 0): [0.06, 0.94], (1, 1): [0.05, 0.95]})\nbn.add_node("J", ["A"], {(0,): [0.95, 0.05], (1,): [0.1, 0.9]})\nbn.add_node("M", ["A"], {(0,): [0.99, 0.01], (1,): [0.3, 0.7]})\n\n\nprint(bn.check_model())\nprint(bn.get_compact())\nprint(bn.get_factors())\nbn.printProbability("A", {"R": 1, "T": 1})\n ```\n\n## Autor\n#### Javier Mombiela',
    'author': 'javim7',
    'author_email': '61723252+javim7@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
