# BNNetwork Library
Esta librería permite crear redes Bayesianas a partir de la probabilidad condicional de cada nodo.

 ## Instalar
`pip install gbnnetwork`

## Uso
Para crear una Red de Inferencia, se deben de seguir los siguientes pasos:
1. Crear una instancia de la clase BNNetwork `network = BNetwork()`
2. Agregar variables a la red `network.add_variable("A")`
3. Asignar los padres de cada variable (en caso la variable no tenga padres este paso se puede omitir) `network.set_parents_to_variable("A", ["B", "E"])`
4. Agregar las probabilidades a las variables para definir la red totalmente. **Toda la red debe de estar definida si se desea responder cualquier consulta** `network.add_probability("A|BE", 0.001)`
5. Hacer una query `p = network.inference({'B': False}, {'A': False})` (Si se desea hacer una query sin valores observados, el diccionario se debe enviar vacío)

## Funciones De Utilidad
1. Obtener la representación compacta `network.compact_string()` (string)
2. Obtener los factores de la red `network.factor_string()` (string)
3. Saber si la red esta totalmente definida `network.validate_defined_state()` (boolean)

## Ejemplo
Tomando como referencia el siguiente documento: https://people.cs.pitt.edu/~milos/courses/cs2740/Lectures/class19.pdf

La red que se propone tiene la siguiente topología:
![Example Network](example_network.png)

Se procede de la siguiente manera:

```python
from gbnnetwork import BNetwork
network = BNetwork()    # Paso 1

# Paso 2
network.add_variable("B")
network.add_variable("E")
network.add_variable("A")
network.add_variable("J")
network.add_variable("M")

# Paso 3
network.set_parents_to_variable("A", ["B", "E"])
network.set_parents_to_variable("J", ["A"])
network.set_parents_to_variable("M", ["A"])

# Paso 4
network.add_probability("B", 0.001)
network.add_probability("E", 0.002)
network.add_probability("A|BE", 0.95)
network.add_probability("A|-BE", 0.29)
network.add_probability("A|B-E", 0.94)
network.add_probability("A|-B-E", 0.001)
network.add_probability("M|A", 0.7)
network.add_probability("M|-A", 0.01)
network.add_probability("J|A", 0.9)
network.add_probability("J|-A", 0.05)

# Hacer la query P(B=True|J=True,M=True)
p = network.inference({'B': True}, {'J': True, 'M': True})  # 0.2841718353643929 = 28%

```
