import curses
import time
import sys

from pip._internal.cli.progress_bars import get_download_progress_renderer

def cli_input(stdscr, prompt):
    curses.use_default_colors()
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    curses.echo()
    curses.cbreak()
    input_str = stdscr.getstr(2, 0, 20)
    curses.echo()
    return input_str.decode("utf-8")

def cli_select(stdscr, prompt, options):
    selected_option = 0
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, -1)

    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    for i, option in enumerate(options):
        if i == selected_option:
            stdscr.addstr(i + 2, 0, f"> {option}", curses.color_pair(1))
        else:
            stdscr.addstr(i + 2, 0, f"  {option}")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and selected_option > 0:
            stdscr.addstr(selected_option+2, 0, f"  {options[selected_option]}")
            selected_option -= 1
            stdscr.addstr(selected_option+2, 0, f"> {options[selected_option]}", curses.color_pair(1))
        elif key == curses.KEY_DOWN and selected_option < len(options) - 1:
            stdscr.addstr(selected_option+2, 0, f"  {options[selected_option]}")
            selected_option += 1
            stdscr.addstr(selected_option+2, 0, f"> {options[selected_option]}", curses.color_pair(1))
        elif key == curses.KEY_ENTER or key in [10, 13]:
            break
    
    return options[selected_option], selected_option
    
def cli_multiselect(stdscr, prompt, options):
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, -1, -1)

    selected_options = []
    current_option = 0

    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    for index, option in enumerate(options):
        if index == current_option:
            color = curses.color_pair(1)
            stdscr.addstr(index+2, 0, f">( ) {option}", color)
        else:
            color = curses.color_pair(2)
            stdscr.addstr(index+2, 0, f" ( ) {option}", color)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_option > 0:
            color = curses.color_pair(2)
            if current_option in selected_options:
                stdscr.addstr(current_option+2, 0, f" (*) {options[current_option]}", color)
            else:
                stdscr.addstr(current_option+2, 0, f" ( ) {options[current_option]}", color)
            
            current_option -= 1
            color = curses.color_pair(1)
            if current_option in selected_options:
                stdscr.addstr(current_option+2, 0, f">(*) {options[current_option]}", color)
            else:
                stdscr.addstr(current_option+2, 0, f">( ) {options[current_option]}", color)

        elif key == curses.KEY_DOWN and current_option < len(options) - 1:
            color = curses.color_pair(2)
            if current_option in selected_options:
                stdscr.addstr(current_option+2, 0, f" (*) {options[current_option]}", color)
            else:
                stdscr.addstr(current_option+2, 0, f" ( ) {options[current_option]}", color)

            current_option += 1
            color = curses.color_pair(1)
            if current_option in selected_options:
                stdscr.addstr(current_option+2, 0, f">(*) {options[current_option]}", color)
            else:
                stdscr.addstr(current_option+2, 0, f">( ) {options[current_option]}", color)
        elif key == 32:
            color = curses.color_pair(1)
            if current_option in selected_options:
                selected_options.remove(current_option)
                stdscr.addstr(current_option+2, 0, f">( ) {options[current_option]}", color)
            else:
                selected_options.append(current_option)
                stdscr.addstr(current_option+2, 0, f">(*) {options[current_option]}", color)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            break

    curses.endwin()

    return [options[i] for i in selected_options], selected_options

def cli_progress(length, progress, prefix, size=60, end=False):
    if progress > length:
        return
    x = int(size*progress/length)
    if progress == length or end:
        print(f"\x1b[2K{prefix} [{'█'*x}{'.'*(size-x)}] {round(100*(progress/length))}%")
    else:
        print(f"\x1b[2K{prefix} [{'█'*x}{'.'*(size-x)}] {round(100*(progress/length))}%", end="\r", flush=True)

def cli_prompt(prompt, options=[], select=False, multiselect=False, options_format=[]): 

    if (multiselect or select) and options == []:
        raise ValueError("Options should not be an empty list if using select or multiselect")
    if multiselect:
        result, index_list = curses.wrapper(cli_multiselect, prompt, options)
        if options_format:
            return [options_format[i] for i in index_list]
        else:
            return result
    elif select:
        result, index = curses.wrapper(cli_select, prompt, options)
        if options_format:
            return (options_format[index])
    else:
        return curses.wrapper(cli_input, prompt)
