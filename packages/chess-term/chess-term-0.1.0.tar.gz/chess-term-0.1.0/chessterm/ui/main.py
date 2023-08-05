import chess
import chess.engine
import click
import curses
from chessterm.ui import TextUI, CursesUI
from chessterm.core import play, Human, Computer


@click.command()
@click.option(
        '--white', '-w',
        type=click.Choice(['human', 'computer']), default='human',
        help='Who is playing as white? (default=human)')
@click.option(
        '--black', '-b',
        type=click.Choice(['human', 'computer']), default='human',
        help='Who is playing as white? (default=human)')
@click.option(
        '--user-interface', '-u',
        type=click.Choice(['text', 'curses']), default='text',
        help='Which user interface? (default=text)')
def ui_main(white, black, user_interface):
    select_ui(white, black, user_interface)


def select_ui(white, black, user_interface):
    view_board_as = (chess.BLACK if white != 'human' and black == 'human'
                     else chess.WHITE)
    if user_interface == 'curses':
        curses.wrapper(curses_main, white, black, view_board_as)
    else:
        do_main(white, black, TextUI(view_board_as))


def curses_main(main_screen, white, black, view_board_as):
    do_main(white, black, CursesUI(main_screen, view_board_as))


def do_main(white, black, ui):
    engine = None
    if 'computer' in [black, white]:
        engine = chess.engine.SimpleEngine.popen_uci('stockfish')
        limit = chess.engine.Limit(time=0.5)
    players = {
            chess.WHITE: Human(ui) if white == 'human' else Computer(engine,
                                                                     limit),
            chess.BLACK: Human(ui) if black == 'human' else Computer(engine,
                                                                     limit)
            }
    play(ui, players)
    if engine:
        engine.quit()
