# Chess Terminal [![pipeline status](https://gitlab.com/OldIronHorse/chess-term/badges/master/pipeline.svg)](https://gitlab.com/OldIronHorse/chess-term/-/commits/master) [![coverage report](https://gitlab.com/OldIronHorse/chess-term/badges/master/coverage.svg)](https://gitlab.com/OldIronHorse/chess-term/-/commits/master)

Play chess in your terminal

## Installation

`pip install chess-term`

For computer play you need the stockfish engine installed

`sudo apt install stockfish`

or

`brew install stockfish`

## Usage

```
Usage: chess-term [OPTIONS]

Options:

  -w, --white [human|computer]    Who is playing as white? (default=human)
  -b, --black [human|computer]    Who is playing as white? (default=human)
  -u, --user-interface [text|curses]
                                  Which user interface? (default=text)
  --help                          Show this message and exit.
```
