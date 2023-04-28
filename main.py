from sys import argv
from playerabstractfactory import ConcreteFactoryWhite, ConcreteFactoryBlue

# GAME_WIDTH = 5
# GAME_HEIGHT = 5

# extending from 0 to 4
# this isn't visually represented correctly, we treat this as height_map[<y_pos>][<x_pos>]
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
        self.game_over = False
        self.positions = DEFAULT_POSITIONS
        self.height_map = DEFAULT_HEIGHT_MAP
    
    def check_for_piece_in_position(self, x_pos, y_pos):
        # position is accessed by giving piece name
        # this reverses it, returning piece by position (if piece is there)
        for item in self.positions.keys():
            if (self.positions[item][0] == x_pos) and (self.positions[item][1] == y_pos):
                return item
        return None

    def check_for_game_over(self):
        # neither of workers can move, they lose
        # if one of your workers are on level three, they win
        pass

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
        self._white_player = ConcreteFactoryWhite().create_human() # white_type).create_human()
        self._blue_player = ConcreteFactoryBlue().create_human() # blue_type).create_human()
        
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
    
    def run(self):
        # print("HELLO")
        # check that not over, while loop
        while self._game.game_over == False:
            self._print_board()
            print(f"Turn: {self._turn}, {repr(self._current_player)}") # DO: put in score
            # this will return a list
            # print(dir(self._current_player))
            new_positions = self._current_player.move(self._game.height_map, self._game.positions) # Q: position of players location? Parameter for move method? What about building towers?
            # input position and board, return new position - maybe do this in game
            # do memento stuff
            # stuff returned from move(), passed into update board
            # update board - input board, return board
            # update turn
            self._turn += 1
            # change current player
            if self._current_player == self._white_player:
                self.current_player = self._blue_player
            else:
                self.current_player = self._white_player

        print("Someone has won") # DO: figure out who won
    
    def _print_board(self):
        for i in range(len(self._game.height_map)):
            print("+--+--+--+--+--+")
            for j in range(len(self._game.height_map[i])):
                print("|", end="")
                # the height map is flipped (y_pos, x_pos)
                print(self._game.height_map[j][i], end="")
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
