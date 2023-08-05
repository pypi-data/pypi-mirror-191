import chess
from chessterm.ui.common import moves_to_text


class TextUI:
    def __init__(self, view_board_as=chess.WHITE):
        self.view_board_as = view_board_as

    def render_board(self, board):
        if self.view_board_as == chess.WHITE:
            for i, row in enumerate(str(board).split('\n')):
                print(f'{8 - i} {row}')
        else:
            for i, row in enumerate(reversed(str(board).split('\n'))):
                print(f'{i + 1} {row}')
        print('  a b c d e f g h')

    def render_moves(self, moves):
        for line in moves_to_text(moves):
            print(line)

    def render_captures(self, pieces):
        print(''.join([p.symbol() for p in pieces]))

    def render_game(self, board, moves, captures):
        self.render_moves(moves)
        self.render_captures(captures[not self.view_board_as])
        self.render_board(board)
        self.render_captures(captures[self.view_board_as])

    def get_move(self, to_move):
        return input(f'{"White" if to_move else "Black"} to move:')

    def render_invalid_move(self, move):
        print(f'Invalid move: {move}')

    def render_result(self, board):
        print('Game over.')
        print(f'Result: {board.result()}')
