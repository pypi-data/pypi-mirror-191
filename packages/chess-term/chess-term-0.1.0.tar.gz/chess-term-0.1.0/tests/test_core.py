import chess
from chessterm.core.core import do_turn, Human


def test_first_turn(mocker):
    ui = mocker.MagicMock()
    white = mocker.MagicMock()
    white.get_move.return_value = chess.Move(chess.E2, chess.E4)
    black = mocker.MagicMock()
    players = {
            chess.WHITE: white,
            chess.BLACK: black,
            }
    board = chess.Board()
    moves = []
    captures = {
            chess.WHITE: [],
            chess.BLACK: [],
            }
    do_turn(ui, players, board, moves, captures)
    assert {chess.WHITE: [], chess.BLACK: []} == captures
    assert ['e4'] == moves
    assert ('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'
            == board.fen())


def test_first_capture(mocker):
    ui = mocker.MagicMock()
    white = mocker.MagicMock()
    white.get_move.return_value = chess.Move(chess.E4, chess.D5)
    black = mocker.MagicMock()
    players = {
            chess.WHITE: white,
            chess.BLACK: black,
            }
    board = chess.Board(
            'rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
    moves = ['e4', 'd5']
    captures = {
            chess.WHITE: [],
            chess.BLACK: [],
            }
    do_turn(ui, players, board, moves, captures)
    assert {
        chess.WHITE: [chess.Piece(chess.PAWN, chess.BLACK)],
        chess.BLACK: [],
        } == captures
    assert ['e4', 'd5', 'exd5'] == moves
    assert ('rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'
            == board.fen())


def test_en_passant(mocker):
    ui = mocker.MagicMock()
    white = mocker.MagicMock()
    black = mocker.MagicMock()
    players = {
            chess.WHITE: white,
            chess.BLACK: black,
            }
    players[chess.BLACK].get_move.return_value = chess.Move(chess.B4,
                                                            chess.C3)
    board = chess.Board(
        'rnbqkbnr/p1pppppp/8/8/1p2P3/5P2/PPPP2PP/RNBQKBNR w KQkq - 0 1')
    board.push_san('c4')
    moves = ['e4', 'b5', 'f3', 'b4', 'c4']
    captures = {
            chess.WHITE: [],
            chess.BLACK: [],
            }
    do_turn(ui, players, board, moves, captures)
    assert {
        chess.WHITE: [],
        chess.BLACK: [chess.Piece(chess.PAWN, chess.WHITE)],
        } == captures
    assert ['e4', 'b5', 'f3', 'b4', 'c4', 'bxc3'] == moves
    assert ('rnbqkbnr/p1pppppp/8/8/4P3/2p2P2/PP1P2PP/RNBQKBNR w KQkq - 0 2'
            == board.fen())


def test_valid_input(mocker):
    ui = mocker.MagicMock()
    ui.get_move.return_value = 'e4'
    human = Human(ui)
    move = human.get_move(chess.Board())
    assert chess.Move(chess.E2, chess.E4) == move


def test_invalid_then_valid(mocker):
    ui = mocker.MagicMock()
    ui.get_move.side_effect = ['e5', 'e4']
    human = Human(ui)
    move = human.get_move(chess.Board())
    assert chess.Move(chess.E2, chess.E4) == move
    ui.render_invalid_move.assert_called_once_with('e5')
