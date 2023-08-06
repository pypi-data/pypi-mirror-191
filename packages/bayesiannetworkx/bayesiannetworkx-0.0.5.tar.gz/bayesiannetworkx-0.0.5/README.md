# Inteligencia Artificial: Laboratorio 2 - Inferencia Probabilistica

## Descripcion 
La clase BayesianNetworkx representa una red bayesiana, un modelo probabilístico que se utiliza en el aprendizaje automático para representar la dependencia entre variables. La clase tiene métodos para agregar nodos a la red, comprobar que la red esté completamente descrita, imprimir la red en forma compacta y en forma de factores, y calcular la probabilidad de un nodo dado un conjunto de evidencia.

- `add_node()`: permite agregar nodos a la red, especificando el nombre del nodo, los padres del nodo y la tabla de probabilidad condicional. 

- `check_model()`: verifica que cada probabilidad en las tablas de probabilidad condicional sumen 1 y que las probabilidades calcuadas sean iguales a las de la tabla con una tolerancia de 0.01. Retorna un booleano:
```python
True
```

- `get_compact()`: imprime la representacio de la red bayesiana en forma compacta. Retorna un string de la siguiente manera:
```python
P(R,T,A,J,M) = P(R)P(T)P(A|R,T)P(J|A)P(M|A)
```

- `get_factors`: Imprime todos los factores de la red bayesiana. Retorna un string de la siguiente manera:
```python
P(R)
  : 0.999, 0.001
P(T)
  : 0.998, 0.002
P(A|R, T)
  0, 0: 0.999, 0.001
  0, 1: 0.71, 0.29
  1, 0: 0.06, 0.94
  1, 1: 0.05, 0.95
P(J|A)
  0: 0.95, 0.05
  1: 0.1, 0.9
P(M|A)
  0: 0.99, 0.01
  1: 0.3, 0.7
```

- `enumarate(variables, evidence)`: Imprime la probabilidad de distribucion de una variable, dado evidencia de otras variables de la red. El parametro de variables, es una lista de las variables de quines obtener los resultados. Y el parametro evidence es un diccionario que contiene los valores de las variables dadas. Ejemplo: `bn.enumarate(["R"], {"J": 1, "M": 1})` Retorna un string de la siguiente manera:
```python
+------+----------+
| A    |   phi(A) |
+======+==========+
| A(0) |    0.050 |
+------+----------+
| A(1) |    0.950 |
+------+----------+
```

## Uso
1. Se debe de importar la libreria bayesiannetworkx.
```python
import bayesiannetworkx as bnx
```

2. Para crear una instancia de la red, no se necesita ningun parametro.
```python
bn = bnx.BayesianNetworkx()
```

3. La red se arma a la hora de crear los nodos y agregarlos a la red. Un nodo consiste de un nombre, una lista de padres, y un diccionario con la tabla de probabilidades. Un nodo tiene que seguir el siguiente formato:
```python
node = {
            "name": name,
            "parents": parents,
            "cpt": cpt,
        }
```

Creando y agregando un nodo sin padres.
```python
bn.add_node("R", [], {(): [0.999, 0.001]})
```
Creando y agregando un nodo con padres. 

```python
bn.add_node("A", ["R", "T"], {(0, 0): [0.999, 0.001], (0, 1): [0.71, 0.29], (1, 0): [0.06, 0.94], (1, 1): [0.05, 0.95]})
```

4. Finalmente, la red esta creada, y se puede utilizar cualquiera de las funciones mencionadas anteriormente para poder obtener la informacion y probabilidades de la red bayesiana. 

## Ejemplo
El siguiente codigo muestra el clasico ejemplo de la alarma. Para este ejemplo debemos de considerar un par de cosas. 
- Tenemos una alarma antirrobo instalada en una casa.
    -  La alarma salta normalmente con la presencia de ladrones.
    - Pero tambien cuando ocurren temblores de tierra.
- Tenemos dos vecinos en la casa, Juan y Maria, que han prometido llamar a la policia si oyen la alarma.
    - Juan y Mara podrian no llamar aunque la alarma sonara: por tener musica muy alta en su casa, por ejemplo.
    - Incluso podran llamar aunque no hubiera sonado: por confundirla con un telefono, por ejemplo.

 Con esta informacion, ya podemos armar la red bayesiana. Siendo "R" el nodo del robo, "T" el nodo del temblor, "A" el nodo de la alarma, "J" el nodo de Juan y "M" el nodo de Maria. 
 ```python
import bayesiannetworkx as bnx

bn = bnx.BayesianNetworkx()

bn.add_node("R", [], {(): [0.999, 0.001]})
bn.add_node("T", [], {(): [0.998, 0.002]})
bn.add_node("A", ["R", "T"], {(0, 0): [0.999, 0.001], (0, 1): [0.71, 0.29], (1, 0): [0.06, 0.94], (1, 1): [0.05, 0.95]})
bn.add_node("J", ["A"], {(0,): [0.95, 0.05], (1,): [0.1, 0.9]})
bn.add_node("M", ["A"], {(0,): [0.99, 0.01], (1,): [0.3, 0.7]})


print(bn.check_model())
print(bn.get_compact())
print(bn.get_factors())
bn.printProbability("A", {"R": 1, "T": 1})
 ```

## Autor
#### Javier Mombiela