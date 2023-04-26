from __future__ import annotations
from abc import ABC, abstractmethod

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
    def __init__(self):
        # Q: better way to do this? want to know the worker names "A", "B"
        self.position_A = DEFAULT_A_POS
        self.position_B = DEFAULT_B_POS

    def create_human(self) -> AbstractPlayerType:
        return ConcreteProductHuman() 
    def create_random(self) -> AbstractPlayerType:
        return ConcreteProductRandom()
    def create_heuristic(self) -> AbstractPlayerType:
        return ConcreteProductHeuristic()

class ConcreteFactoryBlue(AbstractFactory):
    """
    Each Concrete Factory has a corresponding product variant.
    """
    def __init__(self):
        self.position_Y = DEFAULT_Y_POS
        self.position_Z = DEFAULT_Z_POS
    
    def create_human(self) -> AbstractPlayerType:
        return ConcreteProductHuman()
    def create_random(self) -> AbstractPlayerType:
        return ConcreteProductRandom()
    def create_heuristic(self) -> AbstractPlayerType:
        return ConcreteProductHeuristic()

class AbstractPlayerType(ABC):
    """
    Each distinct product of a product family should have a base interface. All
    variants of the product must implement this interface.
    """
    @abstractmethod
    def move(self):
        pass

"""
Concrete Products are created by corresponding Concrete Factories.
"""

class ConcreteProductHuman(AbstractPlayerType):
    def move(self):
        print("Move like a human")

class ConcreteProductRandom(AbstractPlayerType):
    def move(self):
        print("Move like a random")
    
class ConcreteProductHeuristic(AbstractPlayerType):
    def move(self):
        print("Move like a heuristic")

    
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

if __name__ == "__main__":
    # """
    # The client code can work with any concrete factory class.
    # """
    # print("Client: Testing client code with the first factory type:")
    # client_code(ConcreteFactoryWhite())
    # print("\n")
    # print("Client: Testing the same client code with the second factory type:")
    # client_code(ConcreteFactoryBlue())

    blue_player = ConcreteFactoryBlue().create_human()
    white_player = ConcreteFactoryWhite.create_random()
