from itertools import cycle, zip_longest


def moves_to_text(moves):
    white_moves = [move for white, move
                   in zip(cycle([True, False]), moves) if white]
    black_moves = [move for black, move
                   in zip(cycle([False, True]), moves) if black]
    return [f'{i+1:3}. {white_move:6} {black_move}' if black_move
            else f'{i+1:3}. {white_move}'
            for i, (white_move, black_move)
            in enumerate(zip_longest(white_moves, black_moves))]
