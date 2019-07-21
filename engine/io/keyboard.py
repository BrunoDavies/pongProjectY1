import curses


class KeyboardListener:

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.values = {
            "left_player": {
                "delta_y": None,
                "abs_y": None,    # this value will always be None here, it will be
                # used when the input comes from the controller as it will provide
                # an absolute value for the players y position
                "btn_1": False,
                "btn_2": False
            },
            "right_player": {
                "delta_y": None,
                "abs_y": None,    # this value will always be None here, it will be
                # used when the input comes from the controller as it will provide
                # an absolute value for the player's y position
                "btn_1": False,
                "btn_2": False
            }
        }

    def __del__(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def update(self):   
        ch = self.stdscr.getch()



if __name__ == '__main__':
    import time
    kl = KeyboardListener()
    while True:
        #print(get_input())
        kl.update()