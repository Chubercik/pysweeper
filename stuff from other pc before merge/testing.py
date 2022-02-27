import os
import sys

from click.decorators import pass_context

from datatypes import Color, Position

TRANSPARENT = Color(-1, 0, 0)


def draw(color: Color, text_pos: Position, text, textcolor: Color = None):
    """
    Prints text at x, y with background color
    :param text_pos:
    :param color:
    :param text:
    :param textcolor:
    :return:
    """
    # ANSI Escape sequences
    # Somehow this was easier than curses or rich

    # Make text color black if background is too light
    if sum(list(color)) > 350 and textcolor is None:
        text = f"\x1b[38;2;0;0;0m{text}\x1b[0m"
    if textcolor is not None:
        text = f"\x1b[38;2;{textcolor.r};{textcolor.g};{textcolor.b}m{text}\x1b[0m"

    if color is not TRANSPARENT:
        color_start = f"\x1b[48;2;{color.r};{color.g};{color.b}m"
        color_end = "\x1b[0m"
    else:
        color_start = ""
        color_end = ""
    position_start = f"\x1b7\x1b[{text_pos.y};{text_pos.x}f"
    position_end = "\x1b8"
    sys.stdout.write(color_start + position_start + text + position_end + color_end)


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
    import termios
    import tty

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


color1 = Color(255, 255, 255)
color2 = Color(0, 0, 0)
pos1 = Position(10, 10)
pos2 = Position(11, 10)

"""
for i in range(100):
    color1 = Color(255 - 2*i, 255, 255 - i)
    color2 = Color(0, i, 0)
    pos1 = Position(10 + i, 10)
    draw(color1, pos1, chr(33 + i), color2)
"""

clear()
hide_cursor()
draw(color1, pos1, '[', color2)
draw(color1, pos2, ']', color2)
while True:
    m = getch()
    if m.lower() == "w":
        pos1.y -= 1
        pos2.y -= 1
    elif m.lower() == "a":
        pos1.x -= 2
        pos2.x -= 2
    elif m.lower() == "s":
        pos1.y += 1
        pos2.y += 1
    elif m.lower() == "d":
        pos1.x += 2
        pos2.x += 2
    elif m.lower() == "e":
        break
    draw(color1, pos1, ' ', color2)
    draw(color1, pos2, ' ', color2)
    sys.stdout.flush()
