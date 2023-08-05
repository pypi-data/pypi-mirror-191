import chess


def play(ui, players):
    board = chess.Board()
    moves = []
    captures = {
            chess.WHITE: [],
            chess.BLACK: [],
            }
    while not board.is_game_over():
        do_turn(ui, players, board, moves, captures)
    ui.render_game(board, moves, captures)
    ui.render_result(board)


def do_turn(ui, players, board, moves, captures):
    ui.render_game(board, moves, captures)
    move = players[board.turn].get_move(board)
    if board.is_capture(move):
        if board.is_en_passant(move):
            captures[board.turn].append(chess.Piece(chess.PAWN,
                                                    not board.turn))
        else:
            captures[board.turn].append(board.piece_at(move.to_square))
    moves.append(board.san(move))
    board.push_uci(move.uci())


class Computer:
    def __init__(self, engine, limit):
        self.engine = engine
        self.limit = limit

    def get_move(self, board):
        return self.engine.play(board, self.limit).move


class Human:
    def __init__(self, ui):
        self.ui = ui

    def __eq__(self, other):
        try:
            return self.ui == other.ui
        except AttributeError:
            return False

    def get_move(self, board):
        while True:
            m = self.ui.get_move(board.turn)
            try:
                return board.parse_san(m)
            except ValueError:
                self.ui.render_invalid_move(m)
