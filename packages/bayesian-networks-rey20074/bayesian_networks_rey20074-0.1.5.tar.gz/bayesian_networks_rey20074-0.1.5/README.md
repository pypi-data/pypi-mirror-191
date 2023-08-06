# Redes Bayesianas

Una librería para construir redes bayesianas y realizar inferencia probabilística.

## Instalación

Con el manejador de paquetes pip:

- **pip install bayesian-networks-rey20074**

## Uso

<sub> 
    
    from src.bayesian_networks_rey20074.BayesianNetwork import BayesianNetwork, Node

    node_b = Node("b", 0.001)

    node_e = Node("e", 0.002)

    node_a = Node("a", multiple_parents=True)
    node_a.add_connection_multiple_parents({"b": True, "e": True}, 0.95)
    node_a.add_connection_multiple_parents({"b": True, "e": False}, 0.94)
    node_a.add_connection_multiple_parents({"b": False, "e": True}, 0.29)
    node_a.add_connection_multiple_parents({"b": False, "e": False}, 0.001)
    node_a.add_connection("j", 0.9, True)
    node_a.add_connection("j", 0.05, False)
    node_a.add_connection("m", 0.7, True)
    node_a.add_connection("m", 0.01, False)

    node_j = Node("j")
    node_m = Node("m")


    network = BayesianNetwork()
    network.add_node(node_a)
    network.add_node(node_b)
    network.add_node(node_e)
    network.add_node(node_j)
    network.add_node(node_m)
    print('## GET PROBABILISTIC INFERENCE')
    print(network.probabilistic_inference("m"))

    print('\n## GET COMPACT REPRESENTATION')
    representation = network.get_compact_representation()
    print(representation)

    print('## GET ELEMENTS USED FOR ALGORITHM')
    collections = network.get_all_representations()
    for x in collections:
        print(x)

    print('\n## GET IS FULLY DESCRIBED')
    desc = network.is_fully_described()

    if (desc == True):
        print("Red Bayesiana Descriptiva")
    else:
        print("Red Bayesiana No Descriptiva")

</sub>

## API

Se incluyen las siguientes clases

### Clase Node

- **init**(self, title: str, probability_of_success: float = None, multiple_parents: bool = False)
- add_connection(self, next_node_title: str, probability_of_success: float, parent_was_succesful: bool)
- get_children(self)
- get_children_title(self)
- delete_connection(self, node_title: str)
- delete_connection(self, node_title: str, parent_was_succesful: bool)
- add_connection_multiple_parents(self, parent_nodes: dict, probability_of_success: float)
- edit_connection(self, node_title: str, probability_of_success: float)

### Clase BayesianNetwork

- **init**(self)
- get_nodes(self)
- get_node(self, node_title: str)
- delete_node(self, node_title: str)
- add_node(self, node: Node)
- replace_node(self, node_title: str, new_node: Node)
- get_parent(self, child_node_title: str)
- get_parents(self, child_node_title: str)
- one_parent_probabilistic_inference(self, node_title: str
- multiply_list(myList: list)
- multiple_parents_probabilistic_inference(self, node_title: str)
- probabilistic_inference(self, node_title: str)
- get_compact_representation(network)
- is_fully_described(self)
