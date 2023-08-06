import curses

def cli_input(stdscr, prompt):
    curses.use_default_colors()
    curses.curs_set(1)
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    curses.echo()
    curses.cbreak()
    input_str = stdscr.getstr(2, 0, 20)
    curses.echo()
    return input_str.decode("utf-8")

curses.wrapper(cli_input, "aaa")