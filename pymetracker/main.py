import curses


def main():
    COMMAND = ""
    COMMAND_HISTORY = list()

    screen = curses.initscr()
    curses.cbreak()
    curses.noecho()
    screen.keypad(True)
    screen.nodelay(True)

    while True:
        try:
            screen.addstr(curses.LINES-1,0, ">| ")
            screen.addstr(curses.LINES-1,3, COMMAND)

            c = screen.getch()        

            if c == curses.KEY_BACKSPACE:
                curses.endwin()
                break

            if c == curses.KEY_ENTER or c==10 or c==13:
                COMMAND_HISTORY.append(COMMAND)
                COMMAND = ""
            
            elif c > 0 :
                COMMAND = COMMAND + chr(c)
            else:
                pass

            screen.refresh()
            screen.clear()

        except Exception as e:
            print(e)
            curses.endwin()

    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    main()