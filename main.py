#!/usr/bin/python3

from utils import *


def main():
    image_path = sys.argv[1]
    hide_cursor()
    print(get_image_str(image_path))

    input('Press enter to exit...')
    show_cursor()


if __name__ == '__main__':
    main()
