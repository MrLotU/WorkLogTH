from modules.module import Module
from utils import clear, finalize
from time import sleep

class SearchModule(Module):
    """Module for searching entries"""

    SEARCH_MENU = '''Search
==================

Please choose a search option from the list below:
    1. \033[4mC\033[0mreation date
    2. \033[4mT\033[0mime Spent
    3. \033[4mE\033[0mxact search
    4. \033[4mR\033[0megex
    5. \033[4mD\033[0mate range
Or press \033[4mQ\033[0m to go back to the main menu]\n'''

    SEARCH_OPTIONS = {
        1: 'C',
        2: 'T',
        3: 'E',
        4: 'R',
        5: 'D'
    }

    def setup(self):
        clear()
        option = input(self.SEARCH_MENU)
        try:
            option = self.SEARCH_OPTIONS[int(option)]
        except ValueError:
            pass
        
        option = option.upper()
        if option == 'Q':
            print('Returning to main menu')
            return
        elif option == 'C':
            pass
        elif option == 'T':
            pass
        elif option == 'E':
            pass
        elif option == 'R':
            pass
        elif option == 'D':
            pass
        else:
            print('Undefined option! Restarting!')
            sleep(1)