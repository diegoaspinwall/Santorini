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

# DEFAULT_POSITIONS = {
#     "A": [1, 3],
#     "B": [3, 1],
#     "Y": [1, 1],
#     "Z": [3, 3]
# }

class Game:
    def __init__(self):
        self.game_over = False
        # self.positions = DEFAULT_POSITIONS
        self.height_map = DEFAULT_HEIGHT_MAP
    
    def check_for_piece_in_position(self, x_pos, y_pos):
        # position is accessed by giving piece name
        # this reverses it, returning piece by position (if piece is there)
        for item in self.positions.keys():
            if (self.positions[item][0] == x_pos) and (self.positions[item][1] == y_pos):
                return item
        return None
        # pass


class SantoriniCLI:
    def __init__(self, white_type="human", blue_type="human", enable_undo_redo="off", enable_score_disp="off"):
        self._game = Game()
        # define game settings
        self._white_type = white_type
        self._blue_type = blue_type
        self._enable_undo_redo = enable_undo_redo
        self._enable_score_disp = enable_score_disp
        print(self._white_type,
        self._blue_type,
        self._enable_undo_redo,
        self._enable_score_disp)
    
    def run(self):
        # print("HELLO")
        self._print_board()
        # this should be:
        '''
        
        '''
    
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
