from __future__ import annotations
from abc import ABC, abstractmethod
import copy
import random

# DEFAULT_POSITIONS = {
#     "A": [1, 3],
#     "B": [3, 1],
#     "Y": [1, 1],
#     "Z": [3, 3]
# }

# DEFAULT_A_POS = [1, 3]
# DEFAULT_B_POS = [3, 1]
# DEFAULT_Y_POS = [1, 1]
# DEFAULT_Z_POS = [3, 3]

COOR_VALS = {
    "[0, 0]" : 0,
    "[0, 1]" : 0,
    "[0, 2]" : 0,
    "[0, 3]" : 0,
    "[0, 4]" : 0,
    "[1, 0]" : 0,
    "[1, 1]" : 1,
    "[1, 2]" : 1,
    "[1, 3]" : 1,
    "[1, 4]" : 0,
    "[2, 0]" : 0,
    "[2, 1]" : 1,
    "[2, 2]" : 2,
    "[2, 3]" : 1,
    "[2, 4]" : 0,
    "[3, 0]" : 0,
    "[3, 1]" : 1,
    "[3, 2]" : 1,
    "[3, 3]" : 1,
    "[3, 4]" : 0,
    "[4, 0]" : 0,
    "[4, 1]" : 0,
    "[4, 2]" : 0,
    "[4, 3]" : 0,
    "[4, 4]" : 0,
}

INFINITY = 9999999

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
    def create_human(self):
        pass
    @abstractmethod
    def create_random(self):
        pass
    @abstractmethod
    def create_heuristic(self):
        pass

class ConcreteFactoryWhite(AbstractFactory):
    """
    Concrete Factories produce a family of products that belong to a single
    variant. The factory guarantees that resulting products are compatible. Note
    that signatures of the Concrete Factory's methods return an abstract
    product, while inside the method a concrete product is instantiated.
    """
    
    def create_human(self) -> AbstractPlayerTypeWhite:
        return ConcreteProductHumanWhite()
    def create_random(self) -> AbstractPlayerTypeWhite:
        return ConcreteProductRandomWhite()
    def create_heuristic(self) -> AbstractPlayerTypeWhite:
        return ConcreteProductHeuristicWhite()


class ConcreteFactoryBlue(AbstractFactory):
    """
    Each Concrete Factory has a corresponding product variant.
    """
    
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
        # self._numeric_directions = [[0,-1], "ne", "e", "se", "s", "sw", "w", "nw"]
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
    
    def update_positions(self, positions, direction, worker):
        diff_coor = self._cardinal_to_numeric[direction]
        positions[worker][0] = positions[worker][0] + diff_coor[0]
        positions[worker][1] = positions[worker][1] + diff_coor[1]
        return positions
    
    def update_board(self, board, build_dir, positions, worker):
        # print(f"Worker position: {positions[worker]}")
        diff_coor = self._cardinal_to_numeric[build_dir]
        # print(f"Build direction: {build_dir}")
        # print(f"Build direction coor: {diff_coor}")
        el_pos_x = positions[worker][0] + diff_coor[0]
        el_pos_y = positions[worker][1] + diff_coor[1]
        # print(f"el_pos_x, el_pos_y {el_pos_x, el_pos_y}")
        # print(f"Board height there: {board[el_pos_y][el_pos_x]}")
        board[el_pos_y][el_pos_x] += 1
        return board
    
    def give_height_score(self, positions, board):
        height = 0
        for worker in self._workers:
            height += board[positions[worker][1]][positions[worker][0]]
        return height

    def give_center_score(self, positions):
        center_score = 0
        for worker in self._workers:
            center_score += COOR_VALS[str(positions[worker])]
        return center_score

    # def combined_distance_from_foreign_worker(self, worker, positions):
    #     pass

    def give_distance_score(self, positions):
        dist_score = 0
        for worker in self._workers:
            temp = []
            # print(positions)
            for opp_name, op_positions in positions.items():
                if opp_name not in self._workers:
                    x_diff = abs(positions[worker][0] - op_positions[0])
                    y_diff = abs(positions[worker][1] - op_positions[1])
                    temp.append(max(x_diff, y_diff))
            # temp.remove(0)
            # temp.remove(0)
            dist_score += min(temp)
        return dist_score

    def check_valid_direction(self, direction_move):
        return direction_move in self._cardinal_directions

    def give_possible_builds(self, curr_worker_position, curr_board, positions):
        possible_builds = copy.deepcopy(self._cardinal_directions)
        # check not building off edge
        if curr_worker_position[0] == 0:
            for el in ["nw", "w", "sw"]:
                try:
                    possible_builds.remove(el)
                except:
                    pass
        elif curr_worker_position[0] == 4:
            for el in ["ne", "e", "se"]:
                try:
                    possible_builds.remove(el)
                except:
                    pass
        if curr_worker_position[1] == 0:
            for el in ["nw", "n", "ne"]:
                try:
                    possible_builds.remove(el)
                except:
                    pass
        elif curr_worker_position[1] == 4:
            for el in ["sw", "s", "se"]:
                try:
                    possible_builds.remove(el)
                except:
                    pass
        temp = []
        for el in possible_builds:
            coordinates = self._cardinal_to_numeric[el]
            el_pos_x = curr_worker_position[0] + coordinates[0]
            el_pos_y = curr_worker_position[1] + coordinates[1]
            # check not building over level 4
            if curr_board[el_pos_y][el_pos_x] > 3:
                temp.append(el)
            # check not building on occupied square
            # DO: fix this
            for key, value in positions.items():
                if value[0] == el_pos_x and value[1] == el_pos_y:
                    temp.append(el)
        for key in temp:
            try:
                possible_builds.remove(key)
            except:
                pass
        
        return possible_builds

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
        temp = []
        for el in possible_moves:
            coordinates = self._cardinal_to_numeric[el]
            el_pos_x = curr_worker_position[0] + coordinates[0]
            el_pos_y = curr_worker_position[1] + coordinates[1]
            # print(f"worker_coor: {curr_worker_position[0], curr_worker_position[1]}")
            # print(f"diff_coor: {coordinates[0], coordinates[1]}")
            # print(f"surround_coor: {el_pos_x, el_pos_y}")
            # print(f"surround_height: {curr_board[el_pos_y][el_pos_x]}")
            #print()
            if curr_board[el_pos_y][el_pos_x] - current_worker_height > 1:

                    temp.append(el)
        
                # print("second", possible_moves)
            # check you're not moving on a dome
            elif curr_board[el_pos_y][el_pos_x] > 3:
                    temp.append(el)
            
            # check we're not moving on top of other player
            for key, value in positions.items():
                if value[0] == el_pos_x and value[1] == el_pos_y:
                    temp.append(el)
        for key in temp:
            try:
                possible_moves.remove(key)
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
        self._cardinal_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
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
        return "blue (YZ)"
    
    def update_positions(self, positions, direction, worker):
        diff_coor = self._cardinal_to_numeric[direction]
        positions[worker][0] = positions[worker][0] + diff_coor[0]
        positions[worker][1] = positions[worker][1] + diff_coor[1]
        return positions
    
    def update_board(self, board, build_dir, positions, worker):
        # print(f"Worker position: {positions[worker]}")
        diff_coor = self._cardinal_to_numeric[build_dir]
        # print(f"Build direction: {build_dir}")
        # print(f"Build direction coor: {diff_coor}")
        el_pos_x = positions[worker][0] + diff_coor[0]
        el_pos_y = positions[worker][1] + diff_coor[1]
        # print(f"el_pos_x, el_pos_y {el_pos_x, el_pos_y}")
        # print(f"Board height there: {board[el_pos_y][el_pos_x]}")
        board[el_pos_y][el_pos_x] += 1
        return board
    
    def give_height_score(self, positions, board):
        height = 0
        for worker in self._workers:
            height += board[positions[worker][1]][positions[worker][0]]
        return height

    def give_center_score(self, positions):
        center_score = 0
        for worker in self._workers:
            center_score += COOR_VALS[str(positions[worker])]
        return center_score

    def give_distance_score(self, positions):
        dist_score = 0
        for worker in self._workers:
            temp = []
            # print(positions)
            for opp_name, op_positions in positions.items():
                if opp_name not in self._workers:
                    x_diff = abs(positions[worker][0] - op_positions[0])
                    y_diff = abs(positions[worker][1] - op_positions[1])
                    temp.append(max(x_diff, y_diff))
            # temp.remove(0)
            # temp.remove(0)
            dist_score += min(temp)
        return dist_score

    def check_valid_direction(self, direction_move):
        return direction_move in self._cardinal_directions

    def give_possible_builds(self, curr_worker_position, curr_board, positions):
        possible_builds = copy.deepcopy(self._cardinal_directions)
        # check not building off edge
        if curr_worker_position[0] == 0:
            for el in ["nw", "w", "sw"]:
                try:
                    possible_builds.remove(el)
                except:
                    pass
        elif curr_worker_position[0] == 4:
            for el in ["ne", "e", "se"]:
                try:
                    possible_builds.remove(el)
                except:
                    pass
        if curr_worker_position[1] == 0:
            for el in ["nw", "n", "ne"]:
                try:
                    possible_builds.remove(el)
                except:
                    pass
        elif curr_worker_position[1] == 4:
            for el in ["sw", "s", "se"]:
                try:
                    possible_builds.remove(el)
                except:
                    pass
        temp = []
        for el in possible_builds:
            coordinates = self._cardinal_to_numeric[el]
            el_pos_x = curr_worker_position[0] + coordinates[0]
            el_pos_y = curr_worker_position[1] + coordinates[1]
            # check not building over level 4
            if curr_board[el_pos_y][el_pos_x] > 3:
                temp.append(el)
            # check not building on occupied square
            # DO: fix this
            for key, value in positions.items():
                if value[0] == el_pos_x and value[1] == el_pos_y:
                    temp.append(el)
        for key in temp:
            try:
                possible_builds.remove(key)
            except:
                pass
        
        return possible_builds

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
        temp = []
        for el in possible_moves:
            coordinates = self._cardinal_to_numeric[el]
            el_pos_x = curr_worker_position[0] + coordinates[0]
            el_pos_y = curr_worker_position[1] + coordinates[1]
            # print(f"worker_coor: {curr_worker_position[0], curr_worker_position[1]}")
            # print(f"diff_coor: {coordinates[0], coordinates[1]}")
            # print(f"surround_coor: {el_pos_x, el_pos_y}")
            # print(f"surround_height: {curr_board[el_pos_y][el_pos_x]}")
            #print()
            if curr_board[el_pos_y][el_pos_x] - current_worker_height > 1:

                    temp.append(el)
        
                # print("second", possible_moves)
            # check you're not moving on a dome
            elif curr_board[el_pos_y][el_pos_x] > 3:
                    temp.append(el)
            
            # check we're not moving on top of other player
            for key, value in positions.items():
                if value[0] == el_pos_x and value[1] == el_pos_y:
                    temp.append(el)
        for key in temp:
            try:
                possible_moves.remove(key)
            except:
                pass
        
        return possible_moves

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
            if len(worker) == 1 and worker not in "ABYZ":
                print("Not a valid worker")
                continue
            elif len(worker) == 1 and worker not in self._workers:
                print("That is not your worker")
                continue
            break
        while True:
            print("Select a direction to move (n, ne, e, se, s, sw, w, nw)")
            direction = input()
            if not self.check_valid_direction(direction):
                print("Not a valid direction")
                continue
            print(f"possible moves: {self.give_possible_moves(positions[worker], board, positions)}")
            if direction not in self.give_possible_moves(positions[worker], board, positions):
                print(f"Cannot move {direction}")
                continue
            break
        # print("POSITIONS:")
        # print(positions)
        updated_positions = self.update_positions(positions, direction, worker)
        # print("NEW POSITIONS:")
        # print(updated_positions)
        # update position here
        while True:
            print("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
            build_dir = input()
            if not self.check_valid_direction(build_dir):
                print("Not a valid direction")
                continue
            print(f"possible moves: {self.give_possible_builds(positions[worker], board, updated_positions)}")
            if build_dir not in self.give_possible_builds(positions[worker], board, updated_positions):
                print(f"Cannot build {build_dir}")
                continue
            break
        # print(f"BOARD: {board}")
        updated_board = self.update_board(board, build_dir, updated_positions, worker)
        # print(f"UPDATED BOARD: {updated_board}")
        # implement direciton and build to board and positions
        return updated_board, updated_positions
    
    # def build(self, board, pos)

class ConcreteProductRandomWhite(AbstractPlayerTypeWhite):
    def move(self, board, positions):
        temp = []
        for worker in self._workers:
            moves = self.give_possible_moves(positions[worker], board, positions)
            for move in moves:
                temp.append([worker, move])
        chosen_worker, move_direction = random.choice(temp)
        updated_positions = self.update_positions(positions, move_direction, chosen_worker)
        build_choices = self.give_possible_builds(positions[chosen_worker], board, updated_positions)
        build_dir = random.choice(build_choices)
        updated_board = self.update_board(board, build_dir, updated_positions, chosen_worker)
        print(chosen_worker,",",move_direction,",",build_dir)
        return updated_board, updated_positions
    
class ConcreteProductHeuristicWhite(AbstractPlayerTypeWhite):
    def move(self):
        print("Move like a heuristic")
        # create moves list
        # get possible moves
        # calculate score for each move
        # height of three neighbor will have INFINITE score
        # if score higher or equal to moves list, add to list
        # when done, select random from list
        # update positions
        # build randomly
        # update board
        # return updated_bboard, updated_positions


class ConcreteProductHumanBlue(AbstractPlayerTypeBlue):
    def move(self, board, positions):
        while True:
            print("Select a worker to move")
            worker = input()
            if len(worker) == 1 and worker not in "ABYZ":
                print("Not a valid worker")
                continue
            elif len(worker) == 1 and worker not in self._workers:
                print("That is not your worker")
                continue
            break
        while True:
            print("Select a direction to move (n, ne, e, se, s, sw, w, nw)")
            direction = input()
            if not self.check_valid_direction(direction):
                print("Not a valid direction")
                continue
            print(f"possible moves: {self.give_possible_moves(positions[worker], board, positions)}")
            if direction not in self.give_possible_moves(positions[worker], board, positions):
                print(f"Cannot move {direction}")
                continue
            break
        # print("POSITIONS:")
        # print(positions)
        updated_positions = self.update_positions(positions, direction, worker)
        # print("NEW POSITIONS:")
        # print(updated_positions)
        # update position here
        while True:
            print("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
            build_dir = input()
            if not self.check_valid_direction(build_dir):
                print("Not a valid direction")
                continue
            print(f"possible moves: {self.give_possible_builds(positions[worker], board, updated_positions)}")
            if build_dir not in self.give_possible_builds(positions[worker], board, updated_positions):
                print(f"Cannot build {build_dir}")
                continue
            break
        # print(f"BOARD: {board}")
        updated_board = self.update_board(board, build_dir, updated_positions, worker)
        # print(f"UPDATED BOARD: {updated_board}")
        # implement direciton and build to board and positions
        return updated_board, updated_positions

class ConcreteProductRandomBlue(AbstractPlayerTypeBlue):
    def move(self, board, positions):
        temp = []
        for worker in self._workers:
            moves = self.give_possible_moves(positions[worker], board, positions)
            for move in moves:
                temp.append([worker, move])
        chosen_worker, move_direction = random.choice(temp)
        updated_positions = self.update_positions(positions, move_direction, chosen_worker)
        build_choices = self.give_possible_builds(positions[chosen_worker], board, updated_positions)
        build_dir = random.choice(build_choices)
        updated_board = self.update_board(board, build_dir, updated_positions, chosen_worker)
        print(chosen_worker,",",move_direction,",",build_dir)
        return updated_board, updated_positions
    
class ConcreteProductHeuristicBlue(AbstractPlayerTypeBlue):
    def move(self):
        print("Move like a heuristic")
        raise ValueError

