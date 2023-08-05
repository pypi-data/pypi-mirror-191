import pytest
import chess
from chessterm.ui.textui import TextUI


@pytest.fixture()
def textui_input(mocker):
    return mocker.patch('chessterm.ui.textui.input')


@pytest.fixture()
def textui_print(mocker):
    return mocker.patch('chessterm.ui.textui.print')


def test_render_board_starting_position(mocker, textui_print):
    TextUI().render_board(chess.Board())
    textui_print.assert_has_calls([
        mocker.call('8 r n b q k b n r'),
        mocker.call('7 p p p p p p p p'),
        mocker.call('6 . . . . . . . .'),
        mocker.call('5 . . . . . . . .'),
        mocker.call('4 . . . . . . . .'),
        mocker.call('3 . . . . . . . .'),
        mocker.call('2 P P P P P P P P'),
        mocker.call('1 R N B Q K B N R'),
        mocker.call('  a b c d e f g h')])


def test_starting_position_black(mocker, textui_print):
    TextUI(chess.BLACK).render_board(chess.Board())
    textui_print.assert_has_calls([
        mocker.call('1 R N B Q K B N R'),
        mocker.call('2 P P P P P P P P'),
        mocker.call('3 . . . . . . . .'),
        mocker.call('4 . . . . . . . .'),
        mocker.call('5 . . . . . . . .'),
        mocker.call('6 . . . . . . . .'),
        mocker.call('7 p p p p p p p p'),
        mocker.call('8 r n b q k b n r'),
        mocker.call('  a b c d e f g h')])


def test_render_moves_no_moves(textui_print):
    TextUI().render_moves([])
    textui_print.assert_not_called()


def test_render_moves_first_move(textui_print):
    TextUI().render_moves(['e4'])
    textui_print.assert_called_once_with('  1. e4')


def test_render_moves_first_turn(textui_print):
    TextUI().render_moves(['e4', 'e5'])
    textui_print.assert_called_once_with('  1. e4     e5')


def test_render_moves_second_move(mocker, textui_print):
    TextUI().render_moves(['e4', 'e5', 'Nf3'])
    textui_print.assert_has_calls([
        mocker.call('  1. e4     e5'),
        mocker.call('  2. Nf3')])


def test_render_captures_no_pieces(textui_print):
    TextUI().render_captures([])
    textui_print.assert_called_once_with('')


def test_render_captures_first_pawn(textui_print):
    TextUI().render_captures([chess.Piece.from_symbol('P')])
    textui_print.assert_called_once_with('P')


def test_render_captures_two_pieces(textui_print):
    TextUI().render_captures([
        chess.Piece.from_symbol('P'),
        chess.Piece.from_symbol('N')])
    textui_print.assert_called_once_with('PN')


def test_render_invalid_move(textui_print):
    TextUI().render_invalid_move('nonsense')
    textui_print.assert_called_once_with('Invalid move: nonsense')


def test_render_result_draw(mocker, textui_print):
    board = mocker.MagicMock()
    board.result.return_value = '1/2-1/2'
    TextUI().render_result(board)
    textui_print.assert_has_calls([
        mocker.call('Game over.'),
        mocker.call('Result: 1/2-1/2')])


def test_get_move_white_to_move(textui_input):
    textui_input.return_value = 'e4'
    assert 'e4' == TextUI().get_move(chess.WHITE)
    textui_input.assert_called_once_with('White to move:')


def test_render_game_staring_position_as_white(mocker):
    text_ui = mocker.MagicMock()
    text_ui.view_board_as = chess.WHITE
    board = mocker.MagicMock()
    captures = {chess.WHITE: 'white', chess.BLACK: 'black'}
    TextUI.render_game(text_ui, board, 'moves', captures)
    assert [
        mocker.call.render_moves('moves'),
        mocker.call.render_captures('black'),
        mocker.call.render_board(board),
        mocker.call.render_captures('white'),
        ] == text_ui.mock_calls
