import os
import sys


def getch():
    """
    Function used to get keyboard input.
    """
    if os.name != "nt":
        return getch_posix()

    import msvcrt

    while True:
        try:
            return msvcrt.getch().decode()
        except UnicodeDecodeError:  # A keypress couldn't be decoded, ignore it
            continue


def getch_posix():
    import sys
    import tty
    import termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def clear():
    """
    Clear the terminal.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def hide_cursor():
    """
    Hide the cursor.
    """
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    """
    Show the cursor.
    """
    sys.stdout.write("\x1b[?25h")
    sys.stdout.flush()
