import chess
from chessterm.ui.main import select_ui, do_main
from chessterm.core import Human


def test_human_human_text(mocker):
    do_main = mocker.patch('chessterm.ui.main.do_main')
    text_ui = mocker.patch('chessterm.ui.main.TextUI')
    curses_main = mocker.patch('chessterm.ui.main.curses_main')
    text_ui.return_value = mocker.MagicMock()
    select_ui('human', 'human', 'text')
    text_ui.assert_called_once_with(chess.WHITE)
    do_main.assert_called_once_with('human', 'human', text_ui.return_value)
    curses_main.assert_not_called()


def test_human_computer_text(mocker):
    do_main = mocker.patch('chessterm.ui.main.do_main')
    text_ui = mocker.patch('chessterm.ui.main.TextUI')
    curses_main = mocker.patch('chessterm.ui.main.curses_main')
    text_ui.return_value = mocker.MagicMock()
    select_ui('human', 'computer', 'text')
    text_ui.assert_called_once_with(chess.WHITE)
    do_main.assert_called_once_with(
            'human', 'computer', text_ui.return_value)
    curses_main.assert_not_called()


def test_computer_human_text(mocker):
    do_main = mocker.patch('chessterm.ui.main.do_main')
    text_ui = mocker.patch('chessterm.ui.main.TextUI')
    curses_main = mocker.patch('chessterm.ui.main.curses_main')
    text_ui.return_value = mocker.MagicMock()
    select_ui('computer', 'human', 'text')
    text_ui.assert_called_once_with(chess.BLACK)
    do_main.assert_called_once_with(
            'computer', 'human', text_ui.return_value)
    curses_main.assert_not_called()


def test_computer_computer_text(mocker):
    do_main = mocker.patch('chessterm.ui.main.do_main')
    text_ui = mocker.patch('chessterm.ui.main.TextUI')
    curses_main = mocker.patch('chessterm.ui.main.curses_main')
    text_ui.return_value = mocker.MagicMock()
    select_ui('computer', 'computer', 'text')
    text_ui.assert_called_once_with(chess.WHITE)
    do_main.assert_called_once_with(
            'computer', 'computer', text_ui.return_value)
    curses_main.assert_not_called()


def test_do_main_human_human(mocker):
    play = mocker.patch('chessterm.ui.main.play')
    ui = mocker.MagicMock()
    do_main('human', 'human', ui)
    play.assert_called_once_with(
            ui, {chess.WHITE: Human(ui), chess.BLACK: Human(ui)})
