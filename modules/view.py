from time import sleep

from modules.module import Module


class ViewModule(Module):
    """Module for viewing/editing entries"""

    def __init__(self, entries):
        self.index = 0
        self.entries = entries

    VIEW_FORMAT = '''Viewing entries
==================

Press \033[4mN\033[0m for next entry
Press \033[4mP\033[0m for previous entry
Press \033[4mE\033[0m to edit entry
Press \033[4mQ\033[0m to return to main menu
==================

Name: {name}
Time spent: {time}
Date created/edited: {date}
Notes:
{notes}\n\n'''

    def load_entries(self):
        if self.entries == []:
            print('No entries were found.')
            return
        self.entries = [dict(entry) for entry in self.entries]
        action = input(self.VIEW_FORMAT.format(**self.entries[self.index])).upper()

        if action == 'N':
            if self.index == len(self.entries):
                print('Already viewing last entry')
                sleep(1)
            else:
                self.index += 1
            self.load_entries()
        elif action == 'P':
            if self.index == 0:
                sleep(1)
                print('Already viewing first entry')
            else:
                self.index -= 1
            self.load_entries()
        elif action == 'E':
            #TODO: Edit entry
            pass
        elif action == 'Q':
            return
        else:
            print('Invalid option. Restarting')
            sleep(1)
            self.load_entries()
