import sys
import os
from time import sleep
from modules import CreateModule, EditModule, SearchModule

MAIN_MENU = '''Worklog
==================

Please choose an option from the list below:
    1. \033[4mC\033[0mreate a new entry
    2. \033[4mS\033[0mearch an existing entry
    3. \033[4mQ\033[0muit the application

'''

OPTIONS = {
    1: 'C',
    2: 'S',
    3: 'Q'
}

def menu():
    """Displays the menu and redirects to underlaying options"""
    clear()
    ### Get desired option
    option = input(MAIN_MENU)
    try:
        option = OPTIONS[int(option)]
    except ValueError:
        pass

    if option.upper() == 'C':
        ### Create
        clear()
        cm = CreateModule()
        name = input('Give a name for the entry:\t')
        time = input('How many minutes did you spend on this entry:\t')
        notes = input('Please give any other notes:\n')
        cm.create_entry(name=name, time=time, notes=notes)
        print('Created entry!')
        sleep(1)
        menu()
    elif option.upper() == 'S':
        ### Search
        print('Search')
    elif option.upper() == 'Q':
        ### Quit
        finalize()
    else:
        ### Undefined option
        print('Undefined option. Restarting!')
        menu()

def clear():
    """Clear the terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def finalize():
    """Provides a message to the user and cleanly exits the program"""
    print('\nShutting down. We hope to see you again!')
    sys.exit(0)

if __name__ == '__main__':
    ### Clean exits
    try:
        menu()
    except KeyboardInterrupt:
        finalize()
