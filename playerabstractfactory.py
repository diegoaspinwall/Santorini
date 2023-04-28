from __future__ import annotations
from abc import ABC, abstractmethod
import copy

# DEFAULT_POSITIONS = {
#     "A": [1, 3],
#     "B": [3, 1],
#     "Y": [1, 1],
#     "Z": [3, 3]
# }

DEFAULT_A_POS = [1, 3]
DEFAULT_B_POS = [3, 1]
DEFAULT_Y_POS = [1, 1]
DEFAULT_Z_POS = [3, 3]

class AbstractFactory(ABC):
    """
    The Abstract Factory interface declares a set of methods that return
    different abstract products. These products are called a family and are
    related by a high-level theme or concept. Products of one family are usually
    able to collaborate among themselves. A family of products may have several
    variants, but the products of one variant are incompatible with products of
    another.
    """
    @abstractmethod
    def create_human(self) -> AbstractPlayerType:
        pass
    @abstractmethod
    def create_random(self) -> AbstractPlayerType:
        pass
    @abstractmethod
    def create_heuristic(self) -> AbstractPlayerType:
        pass

class ConcreteFactoryWhite(AbstractFactory):
    """
    Concrete Factories produce a family of products that belong to a single
    variant. The factory guarantees that resulting products are compatible. Note
    that signatures of the Concrete Factory's methods return an abstract
    product, while inside the method a concrete product is instantiated.
    """
    # def __init__(self): # , player_type):
    #     # Q: better way to do this? want to know the worker names "A", "B"
    #     # Q: where to store workers?
    #     # self.position_A = DEFAULT_A_POS
    #     # self.position_B = DEFAULT_B_POS
    #     self._workers = "AB"
    #     # if player_type == "human":
    #     #     # self._player = ConcreteProductHuman()
    #     #     self.create_human()
    #     # elif player_type == "random":
    #     #     # self._player = ConcreteProductRandom()
    #     #     self.create_random()
    #     # else:
    #     #     # self._player = ConcreteProductHeuristic()
    #     #     self.create_heuristic()
    
    def create_human(self) -> AbstractPlayerTypeWhite:
        return ConcreteProductHumanWhite()
    def create_random(self) -> AbstractPlayerTypeWhite:
        return ConcreteProductRandomWhite()
    def create_heuristic(self) -> AbstractPlayerTypeWhite:
        return ConcreteProductHeuristicWhite()
    
    # def __repr__(self):
    #     return "white (AB)"


class ConcreteFactoryBlue(AbstractFactory):
    """
    Each Concrete Factory has a corresponding product variant.
    """
    # def __init__(self): #, player_type):
    #     # self.position_Y = DEFAULT_Y_POS
    #     # self.position_Z = DEFAULT_Z_POS
    #     self._workers = "YZ"
    #     # if player_type == "human":
    #     #     self.create_human()
    #     # elif player_type == "random":
    #     #     self.create_random()
    #     # else:
    #     #     self.create_heuristic()
    
    # def __repr__(self):
    #     return "blue (YZ)"
    
    def create_human(self) -> AbstractPlayerTypeBlue:
        return ConcreteProductHumanBlue()
    def create_random(self) -> AbstractPlayerTypeBlue:
        return ConcreteProductRandomBlue()
    def create_heuristic(self) -> AbstractPlayerTypeBlue:
        return ConcreteProductHeuristicBlue()

class AbstractPlayerTypeWhite(ABC):
    """
    Each distinct product of a product family should have a base interface. All
    variants of the product must implement this interface.
    """
    def __init__(self):
        self._workers = "AB"
        self._cardinal_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        self._numeric_directions = [[0,-1], "ne", "e", "se", "s", "sw", "w", "nw"]
        self._cardinal_to_numeric = {
            "n": [0,-1],
            "ne": [1,-1],
            "e": [1,0],
            "se": [1,1],
            "s": [0,1],
            "sw": [-1,1],
            "w": [-1,0],
            "nw": [-1,-1]
        }


    def __repr__(self):
        return "white (AB)"
    
    def check_valid_direction(self, direction_move):
        return direction_move in self._cardinal_directions

    def give_possible_moves(self, curr_worker_position, curr_board, positions):
        '''Takes positions and board. Returns a list of possible directions.'''
        possible_moves = copy.deepcopy(self._cardinal_directions)
        # DO: make this shorter
        # check you're not moving off edge
        if curr_worker_position[0] == 0:
            for el in ["nw", "w", "sw"]:
                try:
                    possible_moves.remove(el)
                except:
                    pass
        elif curr_worker_position[0] == 4:
            for el in ["ne", "e", "se"]:
                try:
                    possible_moves.remove(el)
                except:
                    pass
        if curr_worker_position[1] == 0:
            for el in ["nw", "n", "ne"]:
                try:
                    possible_moves.remove(el)
                except:
                    pass
        elif curr_worker_position[1] == 4:
            for el in ["sw", "s", "se"]:
                try:
                    possible_moves.remove(el)
                except:
                    pass
        
        # check you're not moving two steps up
        current_worker_height = curr_board[curr_worker_position[1]][curr_worker_position[0]]
        for el in possible_moves:
            coordinates = self._cardinal_to_numeric[el]
            el_pos_x = curr_worker_position[0] + coordinates[0]
            el_pos_y = curr_worker_position[1] + coordinates[1]
            if curr_board[el_pos_y][el_pos_x] - current_worker_height > 1:
                possible_moves.remove(el)
            
            # check we're not moving on top of other player
            for worker_position in positions:
                if worker_position[0] == el_pos_x and worker_position[1] == el_pos_y:
                    try:
                        possible_moves.remove(el)
                    except:
                        pass
        
        return possible_moves

    @abstractmethod
    def move(self):
        pass

class AbstractPlayerTypeBlue(ABC):
    """
    Each distinct product of a product family should have a base interface. All
    variants of the product must implement this interface.
    """
    def __init__(self):
        self._workers = "YZ"

    def __repr__(self):
        return "blue (YZ)"

    @abstractmethod
    def move(self):
        pass

"""
Concrete Products are created by corresponding Concrete Factories.
"""

class ConcreteProductHumanWhite(AbstractPlayerTypeWhite):
    def move(self, board, positions):
        while True:
            print("Select a worker to move")
            worker = input()
            if len(worker) == 1 and worker in self._workers:
                break
            print("Not a valid worker")
        while True:
            print("Select a direction to move (n, ne, e, se, s, sw, w, nw)")
            direction = input()
            if not self.check_valid_direction(direction):
                print("Not a valid direction")
                continue
            if direction in self.give_possible_moves(positions[worker], board, positions):
                break
            print(f"Cannot move {direction}")
        # while True:
        #     print("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
        #     worker = input()
        #     if len(worker) == 1 and worker in self._workers:
        #         break
        # implement direciton and build to board and positions
        # return positions
    # def build(self, board, pos)

class ConcreteProductRandomWhite(AbstractPlayerTypeWhite):
    def move(self):
        print("Move like a random")
        raise ValueError
    
class ConcreteProductHeuristicWhite(AbstractPlayerTypeWhite):
    def move(self):
        print("Move like a heuristic")
        raise ValueError


class ConcreteProductHumanBlue(AbstractPlayerTypeBlue):
    def move(self):
        while True:
            print("Select a worker to move")
            worker = input()

class ConcreteProductRandomBlue(AbstractPlayerTypeBlue):
    def move(self):
        print("Move like a random")
        raise ValueError
    
class ConcreteProductHeuristicBlue(AbstractPlayerTypeBlue):
    def move(self):
        print("Move like a heuristic")
        raise ValueError


# def client_code(factory: AbstractFactory) -> None:
#     """
#     The client code works with factories and products only through abstract
#     types: AbstractFactory and AbstractProduct. This lets you pass any factory
#     or product subclass to the client code without breaking it.
#     """
#     product_a = factory.create_product_a()
#     product_b = factory.create_product_b()
#     print(f"{product_b.useful_function_b()}")
#     print(f"{product_b.another_useful_function_b(product_a)}", end="")

# if __name__ == "__main__":
#     # """
#     # The client code can work with any concrete factory class.
#     # """
#     # print("Client: Testing client code with the first factory type:")
#     # client_code(ConcreteFactoryWhite())
#     # print("\n")
#     # print("Client: Testing the same client code with the second factory type:")
#     # client_code(ConcreteFactoryBlue())

#     blue_player = ConcreteFactoryBlue().create_human()
#     white_player = ConcreteFactoryWhite().create_random()
