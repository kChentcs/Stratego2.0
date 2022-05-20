

class Move:
    def __init__(self, piece, square, score = 0):
        self.piece = piece
        self.square = square
        self.score = score

    def __eq__(self, other):
        return self.piece == other.piece and self.square == other.square

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def getWorstMove(moves, ismax):
        worstmovescore = 100000 if ismax else -100000
        worstmove = None
        for m in moves:
            if (ismax and worstmovescore > m.score) or (not ismax and worstmovescore < m.score):
                worstmovescore = m.score
                worstmove = m
        return worstmove