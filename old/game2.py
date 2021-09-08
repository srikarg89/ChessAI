class Game:

    def __init__(self):
        self.board = [['_' for j in range(8)] for i in range(8)]
        self.white_pieces = [...] # Format: [x, y, piece (lowercase if white, uppercase if black)]
        self.black_pieces = [[p[0], 7 - p[1], p[2].upper()] for p in self.white_pieces]
        

    def check_move_valid(self, Kx, Ky):
        # Does it put ur king in check?
        

