import curses
import os
import sys

import numpy as np
from PIL import Image

if os.name == 'nt':
    import ctypes


    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]


def dual_color_str(top_color: np.ndarray, bottom_color: np.ndarray, symbol: str = '▄') -> str:
    """
    Returns a dual color block that represents the top and bottom colors.

    :param top_color: The top color of the block.
    :param bottom_color: The bottom color of the block.
    :param symbol: The symbol to use for the block (default to ▄).
    :return: A truecolor ANSI string that represents the dual color block.
    """
    top_red, top_green, top_blue = top_color
    bottom_red, bottom_green, bottom_blue = bottom_color
    top = f'\033[48;2;{top_red};{top_green};{top_blue}m'
    bottom = f'\033[38;2;{bottom_red};{bottom_green};{bottom_blue}m'
    return top + bottom + symbol + '\033[0m'


def get_image_str(image_path: str) -> str:
    row, column = os.get_terminal_size()
    column *= 2
    column -= 2
    image_str = []
    test_image = Image.open(os.path.join(os.getcwd(), image_path)).resize((row, column))
    for i in range(0, test_image.size[1], 2):
        for j in range(test_image.size[0]):
            top_pixel = test_image.getpixel((j, i))
            bottom_pixel = test_image.getpixel((j, i + 1))
            image_str.append(dual_color_str(top_pixel, bottom_pixel))

    test_image.close()

    return ''.join(image_str)


def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
