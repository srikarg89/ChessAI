from helpers import *

def get_possible_moves_loop(x, y, dx, dy):
    poss = []
    curr = (x, y)
    for d in range(1, 9):
        curr = add(curr, (dx, dy))
        if not in_bounds(curr) or teammate_present(curr):
            break
        poss.append(curr) # Include the position that hits an enemy (useful for seeing what ur attacking)
        if not is_clear(curr):
            break
    return poss

def teammate_present(pos):
    # TODO: Implement this
    pass

def is_clear(pos):
    # TODO: Implement this
    pass

class Piece:
    def __init__(self, color, pos, typ):
        self.color = color
        self.pos = pos
        self.type = typ

    def get_move_locs(self):
        raise Exception("Move locs method unimplemented!")


class Pawn(Piece):
    def __init(self, color, pos):
        super.__init__(color, pos, 'p')
        self.move_locs = self.get_move_locs()
        self.attack_locs = self.get_attack_locs()
        self.backrank = 0 if self.color == Color.WHITE else 7
        self.direction = 1 if self.color == Color.WHITE else -1
    
    def get_attack_locs(self):
        attack = []
        if self.pos[0] != 0:
            attack.append(add(self.pos, (-1, direction)))
        if self.pos[0] != 7:
            attack.append(add(self.pos, (1, direction)))
        return attack

    def get_move_locs(self):
        move = []
        target = add(self.pos, (0, self.direction))
        if is_clear(target):
            move.append(target)
            if self.pos[1] == self.backrank + self.direction: # If you haven't moved yet, you can double move
                target = add(target, (0, self.direction))
                if is_clear(target):
                    move.append(target)
        return move


class Knight(Piece):
    def __init(self, color, pos):
        super.__init__(color, pos, 'n')
        self.move_locs = self.get_move_locs()
        self.attack_locs = self.get_attack_locs()
    
    def get_move_locs(self):
        attack = []
        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                target = add(self.pos, (dx, dy))
                if abs(dx) == abs(dy):
                    continue
                if not self.in_bounds(target) or teammate_present(target):
                    continue
                attack.append(add(self.pos, (dx, dy)))
        return attack


class Bishop(Piece):
    def __init(self, color, pos):
        super.__init__(color, pos, 'b')
        self.move_locs = self.get_move_locs()
        self.attack_locs = self.get_attack_locs()
    
    def get_move_locs(self):
        poss = get_possible_moves_loop(self.pos[0], self.pos[1], -1, -1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], -1, 1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], 1, -1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], 1, 1)
        return poss


class Rook(Piece):
    def __init(self, color, pos):
        super.__init__(color, pos, 'r')
        self.move_locs = self.get_move_locs()
        self.attack_locs = self.get_attack_locs()
    
    def get_move_locs(self):
        poss = get_possible_moves_loop(self.pos[0], self.pos[1], 0, -1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], 0, 1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], -1, 0)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], 1, 0)
        return poss


class Queen(Piece):
    def __init(self, color, pos):
        super.__init__(color, pos, 'q')
        self.move_locs = self.get_move_locs()
        self.attack_locs = self.get_attack_locs()
    
    def get_move_locs(self):
        poss = get_possible_moves_loop(self.pos[0], self.pos[1], -1, -1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], -1, 0)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], -1, 1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], 0, -1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], 0, 1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], 1, -1)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], 1, 0)
        poss += get_possible_moves_loop(self.pos[0], self.pos[1], 1, 1)
        return poss


class King(Piece):
    def __init(self, color, pos):
        super.__init__(color, pos, 'k')
        self.move_locs = self.get_move_locs()
        self.attack_locs = self.get_attack_locs()
    
    def get_move_locs(self):
        poss = []
        for dxdy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            target = add(self.pos, dxdy)
            if not in_bounds(target) or teammate_present(target):
                continue
            poss.append(target)
        return poss


