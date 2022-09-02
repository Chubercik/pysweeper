<p align="center">
  <img width="64" src="icon.ico" alt="pysweeper logo">
  <h1 align="center">pysweeper</h1>
  <h6 align="center">a Minesweeper clone written in Python</h6>
</p>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/Chubercik/pysweeper">
  <img src="https://img.shields.io/github/contributors/Chubercik/pysweeper">
  <img src="https://img.shields.io/github/issues/Chubercik/pysweeper">
  <img src="https://img.shields.io/github/stars/Chubercik/pysweeper">
  <img src="https://img.shields.io/github/license/Chubercik/pysweeper">
</p>

<p align="center">
  <h5 align="center">⚠ Work In Progress ⚠</h5>
</p>

**Pysweeper** (onward stylized as `pysweeper` and pronounced `paɪˈswiːpə`) is a clone
of a classic single-player puzzle video game - [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game)),
written in [Python](https://www.python.org/).

There are binaries for Windows available thanks
to the [Nuitka](https://nuitka.net/) transpiler.

Linux binaries have been discontinued due to their large size,
but you can still download the source code and compile it yourself,
if for whatever reason you might feel like it.

## Project structure

    .
    ├── data                     # folder containing game data
    │   ├── config.json          # game configuration
    │   └── data.json            # player scores
    ├── fonts                    # folder containing font files
    ├── modules                  # folder containing DLL files for Nuitka
    ├── sounds                   # folder containing sound files
    ├── textures                 # folder containing texture files
    ├── .gitignore               # ignore list for git
    ├── file_io.py               # script containing file I/O
    ├── icon.ico                 # icon for the game
    ├── LICENSE                  # MIT license
    ├── main.py                  # main script
    ├── nuitka.txt               # file containing Nuitka commands
    ├── pysweeper.py             # pysweeper game script
    ├── README.md                # README file
    ├── requirements.txt         # project dependencies
    ├── sprites.py               # script for sprite loading
    └── utilities.py             # script containing utility functions

## Building

// todo

## Contributing

// todo

<!--
TODO - refactoring:

utilities.py | WIP - refactor fundamental classes,
                     add complex classes (e.g. full Timer class,
                     as opposed to just one digit)
sprites.py   | OK (for the time being)
pysweeper.py | WIP - a lot of things need to be refactored
main.py      | WIP - change the way the game is initialized
file_io.py   | OK 

-->
