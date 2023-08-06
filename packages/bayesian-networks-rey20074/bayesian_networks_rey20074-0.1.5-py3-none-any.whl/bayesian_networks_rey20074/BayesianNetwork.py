class Node:
    def __init__(
        self,
        title: str,
        probability_of_success: float = None,
        multiple_parents: bool = False,
    ):
        self.title = title
        self.connections = []
        self.multiple_parents = multiple_parents
        self.multiple_parents_connections = []

        if probability_of_success is not None:
            if probability_of_success > 1 or probability_of_success < 0:
                raise ValueError("This probability of success is wrong")

            self.success = probability_of_success
            self.fail = 1 - probability_of_success
        else:
            self.success = None
            self.fail = None

    def add_connection(
        self,
        next_node_title: str,
        probability_of_success: float,
        parent_was_succesful: bool,
    ):
        connection = list(
            filter(
                lambda x: next_node_title == x["title"]
                and parent_was_succesful == x["parent_success"],
                self.connections,
            )
        )
        if probability_of_success > 1 or probability_of_success < 0:
            print('Probability "' + str(probability_of_success) + '" cant be used.')
            return False

        if type(parent_was_succesful) != bool:
            print(
                "You need to provide true or false depending on wether the parent was succesful or not"
            )
            return False

        if not connection:
            self.connections.append(
                {
                    "title": next_node_title,
                    "parent_success": parent_was_succesful,
                    "success": probability_of_success,
                    "fail": 1 - probability_of_success,
                }
            )
            return True

        else:
            print(
                'The node "'
                + self.title
                + '" already has a connection to "'
                + next_node_title
                + '"'
            )
            return False

    def get_children(self):
        return self.connections

    def get_children_title(self):
        return list(set([connection["title"] for connection in self.connections]))

    def delete_connection(self, node_title: str):
        before_i = len(self.connections)
        self.connections = list(
            filter(
                lambda connection: node_title != connection["title"], self.connections
            )
        )

        if before_i == len(self.connections):
            print(
                'There is no connection from node "'
                + self.title
                + '" to node "'
                + node_title
                + '".'
            )
            return False

        return True

    def delete_connection(self, node_title: str, parent_was_succesful: bool):
        before_i = len(self.connections)
        self.connections = list(
            filter(
                lambda connection: node_title != connection["title"]
                and parent_was_succesful != connection["parent_success"],
                self.connections,
            )
        )

        if before_i == len(self.connections):
            print(
                'There is no connection from node "'
                + self.title
                + '" to node "'
                + node_title
                + '".'
            )
            return False

        return True

    def add_connection_multiple_parents(
        self, parent_nodes: dict, probability_of_success: float
    ):
        if probability_of_success > 1 or probability_of_success < 0:
            print('Probability "' + str(probability_of_success) + '" cant be used.')
            return False

        if len(parent_nodes.values()) <= 1:
            print(
                "You should use this function when there is a connection of more than 2 nodes, use add_connection() over the parent of this node instead"
            )
            return False

        for value in parent_nodes.values():
            if type(value) is not bool:
                print(
                    "You need to provide true or false depending on wether the parent was succesful or not"
                )
                return False

        new_multiple_connection = {
            **parent_nodes,
            **{"success": probability_of_success, "fail": 1 - probability_of_success},
        }

        remodeled_connections = [
            {field: connection[field] for field in list(connection.keys())[0:-2]}
            for connection in self.multiple_parents_connections
        ]

        if parent_nodes in remodeled_connections:
            print(
                'The node "'
                + self.title
                + '" already has a parent connection "'
                + str(parent_nodes)
                + '"'
            )
            return False

        self.multiple_parents_connections.append(new_multiple_connection)
        return True

    def edit_connection(self, node_title: str, probability_of_success: float):
        res = self.delete_connection(node_title)
        if res:
            res = self.add_connection(node_title, probability_of_success)
        return res


class BayesianNetwork:
    def __init__(self):
        self.nodes = []

    def get_nodes(self):
        return self.nodes

    def get_node(self, node_title: str):
        return list(filter(lambda node: node_title == node.title, self.nodes))[0]

    def delete_node(self, node_title: str):
        before_i = len(self.nodes)
        self.nodes = list(filter(lambda node: node_title != node.title, self.nodes))
        if before_i == len(self.nodes):
            print('No nodes with title "' + node_title + '" were found.')
            return False
        return True

    def add_node(self, node: Node):
        nodes = list(filter(lambda x: node.title == x.title, self.nodes))
        if not nodes:
            self.nodes.append(node)
            return True
        else:
            print('Node "' + node.title + '" already exists on network')
            return False

    def replace_node(self, node_title: str, new_node: Node):
        res = self.delete_node(node_title)
        if res:
            self.add_node(new_node)
        return res

    def get_parent(self, child_node_title: str):
        return list(
            set(
                filter(
                    lambda node: child_node_title in node.get_children_title(),
                    self.nodes,
                )
            )
        )

    def get_parents(self, child_node_title: str):
        current_node = self.get_node(child_node_title)

        connections = []

        for connection in current_node.multiple_parents_connections:
            connections += list(connection.keys())[0:-2]

        connections = list(set(connections))

        return list(set(filter(lambda node: node.title in connections, self.nodes)))

    def one_parent_probabilistic_inference(self, node_title: str):
        parent = self.get_parent(node_title)[0]

        parent_probability = self.probabilistic_inference(parent.title)

        if not parent_probability:
            return False

        connections = list(
            filter(
                lambda connection: connection["title"] == node_title, parent.connections
            )
        )

        if len(connections) < 2:
            print(
                'The amount of connections parent "'
                + parent.title
                + '" have to node "'
                + node_title
                + '" arent enough.\n'
            )
            return False

        success_probability = 0
        fail_probability = 0

        for connection in connections:
            if connection["parent_success"]:
                success_probability += (
                    parent_probability["success"] * connection["success"]
                )
                fail_probability += parent_probability["success"] * connection["fail"]
            else:
                success_probability += (
                    parent_probability["fail"] * connection["success"]
                )
                fail_probability += parent_probability["fail"] * connection["fail"]

        if success_probability + fail_probability < 0.95:
            print(
                'Something went wrong when calculating the probability, currently on node "'
                + node_title
                + '"'
            )
            return False

        return {"success": success_probability, "fail": fail_probability}

    def multiply_list(myList: list):
        result = 1
        for i in range(0, len(myList)):
            result = result * myList[i]
        return result

    def multiple_parents_probabilistic_inference(self, node_title: str):
        current_node = self.get_node(node_title)
        parents = self.get_parents(node_title)
        parent_probabilities = []
        for parent in parents:
            parent_probabilities.append(
                {parent.title: self.probabilistic_inference(parent.title)}
            )

        success_probability = 0
        fail_probability = 0

        for connection in current_node.multiple_parents_connections:
            calculation_probabilites = []
            for parent_index in range(0, len(parents)):
                if connection[parents[parent_index].title]:
                    calculation_probabilites.append(
                        parent_probabilities[parent_index][parents[parent_index].title][
                            "success"
                        ]
                    )
                else:
                    calculation_probabilites.append(
                        parent_probabilities[parent_index][parents[parent_index].title][
                            "fail"
                        ]
                    )

            probability_result = 1
            for i in range(0, len(calculation_probabilites)):
                probability_result *= calculation_probabilites[i]

            success_probability += probability_result * connection["success"]
            fail_probability += probability_result * connection["fail"]

        return {"success": success_probability, "fail": fail_probability}

    def probabilistic_inference(self, node_title: str):
        current_node = self.get_node(node_title)

        if current_node.success is not None:
            return {"success": current_node.success, "fail": current_node.fail}

        if current_node.multiple_parents:
            return self.multiple_parents_probabilistic_inference(node_title)
        else:
            return self.one_parent_probabilistic_inference(node_title)

    def get_compact_representation(self):
        representation = ""
        nodes = self.get_nodes()

        for node in nodes:
            if node.get_children():
                representation += (
                    node.title
                    + " -> "
                    + ", ".join(list(set([child["title"] for child in node.get_children()])))
                    + "\n"
                )
            if node.multiple_parents:
                for parent in self.get_parents(node.title):
                    representation += (
                        parent.title
                        + " -> "
                        + node.title
                        + "\n"
                    )
        return representation
    
    def get_all_representations(self):
        colections = []
        for node in self.nodes:
            colections += node.connections
            colections += node.multiple_parents_connections
        return [col for col in colections if col != []]


    def is_fully_described(self):
        for node in self.nodes:
            if len(node.connections) == 0:
                return False
            for connection in node.connections:
                if connection["success"] + connection["fail"] != 1:
                    return False
        return True
