import curses
from curses.textpad import Textbox, rectangle
import chess
from chessterm.ui.common import moves_to_text


class CursesUI:
    def __init__(self, main_screen, view_board_as):
        self.main_screen = main_screen
        self.view_board_as = view_board_as
        max_y, max_x = main_screen.getmaxyx()
        curses.curs_set(False)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
        self.win_board = curses.newwin(11, 19, 2, 0)
        self.win_moves = curses.newwin(max_y, 20, 0, 20)
        self.win_captures_black = curses.newwin(2, 16, 0, 2)
        self.win_captures_white = curses.newwin(2, 16, 13, 2)
        self.win_result = curses.newwin(1, 19, max_y - 1, 0)
        self.win_prompt = curses.newwin(0, 19, 15, 0)
        self.win_input = curses.newwin(1, 17, 17, 1)
        self.textbox_input = Textbox(self.win_input)
        self.main_screen.noutrefresh()

    def render_game(self, board, moves, captures):
        self.render_board(board)
        self.render_moves(moves)
        self.render_captures(self.win_captures_black, captures[chess.BLACK])
        self.render_captures(self.win_captures_white, captures[chess.WHITE])
        curses.doupdate()

    def render_board(self, board):
        self.win_board.clear()
        self.win_board.border()
        for row, n in zip(range(1, 10), range(8, 0, -1)):
            self.win_board.addstr(row, 1, f'{n}')
        self.win_board.addstr(9, 1, '  a b c d e f g h')
        square_colour = 1
        for row in range(0, 8):
            for col in range(0, 8):
                p = board.piece_at(chess.square(col, row))
                if p:
                    self.win_board.addstr(
                            8 - row, (col * 2) + 2,
                            f'{p.unicode_symbol(invert_color=True)} ',
                            curses.color_pair(square_colour))
                else:
                    self.win_board.addstr(8 - row, (col * 2) + 2,
                                          '  ',
                                          curses.color_pair(square_colour))
                square_colour = 2 if square_colour == 1 else 1
            square_colour = 2 if square_colour == 1 else 1
        self.win_board.noutrefresh()

    def render_moves(self, moves):
        self.win_moves.clear()
        max_y, max_x = self.win_moves.getmaxyx()
        for i, line in enumerate(moves_to_text(moves)[-max_y:]):
            self.win_moves.addstr(i, 0, line)
        self.win_moves.noutrefresh()

    def render_captures(self, window, pieces):
        window.clear()
        window.addstr(0, 0, ' '.join([p.unicode_symbol(invert_color=True)
                                      for p in pieces[:8]]))
        window.addstr(1, 0, ' '.join([p.unicode_symbol(invert_color=True)
                                      for p in pieces[8:]]))
        window.noutrefresh()

    def render_result(self, board):
        curses.curs_set(True)
        self.win_result.addstr(0, 0, f'Game over: {board.result()}')
        self.win_result.getch()

    def get_move(self, to_play):
        to_play = 'White' if to_play else 'Black'
        self.win_prompt.addstr(0, 0, f'{to_play} to play:')
        self.win_prompt.refresh()
        rectangle(self.main_screen, 16, 0, 18, 18)
        self.main_screen.refresh()
        curses.curs_set(True)
        self.textbox_input.edit()
        curses.curs_set(False)
        move = self.textbox_input.gather()
        self.win_input.clear()
        return move.strip()

    def render_invalid_move(self, move):
        # TODO; display invalid move message
        pass
