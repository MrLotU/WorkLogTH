import sys
import os


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
    ### Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    ### Get desired option
    option = input(MAIN_MENU)
    try:
        option = OPTIONS[int(option)]
    except ValueError:
        pass

    if option == 'C':
        ### Create
        print('Create')
    elif option == 'S':
        ### Search
        print('Search')
    elif option == 'Q':
        ### Quit
        finalize()
    else:
        ### Undefined option
        print('Undefined option. Restarting!')
        menu()

def finalize():
    """Provides a message to the user and cleanly exits the program"""
    print('Shutting down. We hope to see you again!')
    sys.exit(0)

if __name__ == '__main__':
    ### Python 2 compatibility
    try:
        input = raw_input
    except NameError:
        pass
    ### Clean exits
    try:
        menu()
    except KeyboardInterrupt:
        finalize()
