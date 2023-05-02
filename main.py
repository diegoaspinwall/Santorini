from sys import argv
from playerabstractfactory import ConcreteFactoryWhite, ConcreteFactoryBlue

# GAME_WIDTH = 5
# GAME_HEIGHT = 5

# extending from 0 to 4
# this isn't visually represented correctly, but use as height_map[<x_pos>][<y_pos>]
DEFAULT_HEIGHT_MAP = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

DEFAULT_POSITIONS = {
    "A": [1, 3],
    "B": [3, 1],
    "Y": [1, 1],
    "Z": [3, 3]
}

class Game:
    def __init__(self):
        # self.game_over = False
        self.winner = None
        self.positions = DEFAULT_POSITIONS
        self.height_map = DEFAULT_HEIGHT_MAP
    
    def check_for_piece_in_position(self, x_pos, y_pos):
        # position is accessed by giving piece name
        # this reverses it, returning piece by position (if piece is there)
        for item in self.positions.keys():
            if (self.positions[item][0] == x_pos) and (self.positions[item][1] == y_pos):
                return item
        return None

    def check_for_winner(self, white_player, blue_player):
        # if one of your workers are on level three, they win
        # get worker names from player
        print( self.positions["A"])
        workers = white_player._workers
        # check positions for each worker
        for worker in workers:
            worker_pos = self.positions[worker]
            print(worker, self.positions[worker])
            # find height there
            # if self.height_map[worker_pos[0]][worker_pos[1]] == 3:
            if self.height_map[worker_pos[1]][worker_pos[0]] == 3:
                # if height == 3, they win
                print(self.height_map[worker_pos[0]][worker_pos[1]])
                print(worker_pos[0],worker_pos[1])
                print("white has won")
                return True
        # ^^ do for both
        blue_workers = blue_player._workers
        # check positions for each worker
        for worker in blue_workers:
            worker_pos = self.positions[worker]
            # find height there
            # if self.height_map[worker_pos[0]][worker_pos[1]] == 3:
            if self.height_map[worker_pos[1]][worker_pos[0]] == 3:
                # if height == 3, they win
                print("blue has won")
                return True
        return False

    def check_for_loser(self, curr_player):
        # neither of workers can move, they lose
        # get worker names from player
        # call give_possible_moves on each worker
        # if both lists are empty, other player wins
        # curr_worker_position, curr_board, positions):
        workers = curr_player._workers
        # check positions for each worker
        for worker in workers:
            if curr_player.give_possible_moves(self.positions[worker], self.height_map, self.positions) != []:
                return False
        return True

    def update_board(self):
        pass


class SantoriniCLI:
    def __init__(self, white_type="human", blue_type="human", enable_undo_redo="off", enable_score_disp="off"):
        self._game = Game()
        self._turn = 1
        # define game settings
        '''
        blue_player = ConcreteFactoryBlue().create_human()
        white_player = ConcreteFactoryWhite().create_random()
        '''
        if white_type == "human":
            self._white_player = ConcreteFactoryWhite().create_human()
        elif white_type == "random":
            self._white_player = ConcreteFactoryWhite().create_random()
        else:
            self._white_player = ConcreteFactoryWhite().create_heuristic()

        if blue_type == "human":
            self._blue_player = ConcreteFactoryBlue().create_human()
        elif blue_type == "random":
            self._blue_player = ConcreteFactoryBlue().create_random()
        else:
            self._blue_player = ConcreteFactoryBlue().create_heuristic()
        
        # if white_type == "human":
        #     # self._white_player.create_human()
        #     self._white_player = ConcreteFactoryWhite().create_human()
        # else:
        #     raise "Add functionality for this"
        
        # if blue_type == "human":
        #     self._blue_player = ConcreteFactoryBlue().create_human()
        # else:
        #     raise "Add functionality for this"
        
        self._current_player = self._white_player

        self._enable_undo_redo = enable_undo_redo
        self._enable_score_disp = enable_score_disp

        print(white_type,
        blue_type,
        self._enable_undo_redo,
        self._enable_score_disp)
        print()

    def print_turn_details(self):
        height_score = self._current_player.give_height_score(self._game.positions, self._game.height_map)
        center_score = self._current_player.give_center_score(self._game.positions)
        distance_score = self._current_player.give_distance_score(self._game.positions)
        print(f"Turn: {self._turn}, {repr(self._current_player)}", end = "")
        if self._enable_score_disp != "off":
            print(f", ({height_score}, {center_score}, {distance_score})", end = "")
        print()
    
    def run(self):
        # print("HELLO")
        self._print_board()
        self.print_turn_details()
        # check that not over, while loop
        # while self._game.game_over == False:
        # while self._game.winner == None:
        while True:
            # check for game over
            if self._game.check_for_winner(self._white_player, self._blue_player) == True:
                break
            if self._game.check_for_loser(self._current_player) == True: # self._white_player, self._blue_player)
                if self._current_player == self._white_player:
                    print("blue has won")
                else:
                    print("white has won")
                break
            # move worker and build
            new_board, new_positions = self._current_player.move(self._game.height_map, self._game.positions)
            # DO: memento stuff
            self._game.height_map = new_board
            self._game.positions = new_positions
            # update turn
            self._turn += 1
            # change current player
            if self._current_player == self._white_player:
                # print("DID THIS")
                self._current_player = self._blue_player
            else:
                # print("DID THAT")
                self._current_player = self._white_player
            # print("NEW PLAYER")
            # print(dir(self.current_player))
            self._print_board()
            self.print_turn_details()
    
    def _print_board(self):
        for i in range(len(self._game.height_map)):
            print("+--+--+--+--+--+")
            for j in range(len(self._game.height_map[i])):
                print("|", end="")
                # the height map is (x_pos, y_pos)
                print(self._game.height_map[i][j], end="")
                piece_at_position = self._game.check_for_piece_in_position(j, i)
                if piece_at_position == None:
                    print(" ", end="")
                else:
                    print(piece_at_position, end="")
            print("|")
        print("+--+--+--+--+--+")


if __name__ == "__main__":
    # print(argv)
    # my_santorini_instance = SantoriniCLI(argv[1], argv[2], argv[3], argv[4])
    my_santorini_instance = SantoriniCLI(*argv[1:])
    my_santorini_instance.run()
