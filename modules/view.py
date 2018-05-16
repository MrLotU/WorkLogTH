import shutil
from csv import DictReader, DictWriter
from datetime import datetime
from time import sleep

from modules.module import Module
from utils import clear


class ViewModule(Module):
    """Module for viewing/editing entries"""

    def __init__(self, entries):
        self.index = 0
        ### Convert entries to normal dicts instead of OrderedDict
        self.entries = [dict(entry) for entry in entries]

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
        """Show an entry along with the options to the user"""
        ### Clear the screen
        clear()
        ### Check if we have entries
        ### Otherwise, return
        if self.entries == []:
            print('No entries were found.')
            return
        ### Get user input
        action = input(self.VIEW_FORMAT.format(**self.entries[self.index])).upper()

        ### Check user input
        if action == 'N':
            ### Check if we're on the last entry
            ### If not, increment index and reload
            if self.index >= len(self.entries) - 1:
                print('Already viewing last entry')
                sleep(1)
            else:
                self.index += 1
            self.load_entries()
        elif action == 'P':
            ### Check if we're on the first entry
            ### If not, decrement index and reload
            if self.index == 0:
                print('Already viewing first entry')
                sleep(1)
            else:
                self.index -= 1
            self.load_entries()
        elif action == 'E':
            ### Start editing process for selected entry
            entry = self.entries[self.index]
            line = entry['line']
            self.update_row(line, entry)
        elif action == 'Q':
            ### Return to main menu
            return
        else:
            ### Restart setup
            print('Invalid option. Restarting')
            sleep(1)
            self.load_entries()

    def update_row(self, index, row):
        """Editing flow"""
        ### Clear the screen
        clear()
        ### Set the new date
        updates = {'date': datetime.utcnow().strftime('%m/%d/%Y')}
        ### Get and validate user input
        name = input(
            'Current title is: {}. If you want to edit, give a new title. Otherwise leave this empty\t'.format(
                row['name']
            )
        )
        if not name == '':
            updates['name'] = name
        time = input(
            'Current time spent is: {}. If you want to edit, give a new time spent. Otherwise leave this empty\t'.format(
                row['time']
            )
        )
        if not time == '':
            try:
                int(time)
            except ValueError:
                print('Invalid time provided. Not changing the value')
            else:
                updates['time'] = time
        notes = input(
            'Current notes are: \n{}\nIf you want to edit, give new notes. Otherwise leave this empty\n'.format(
                row['notes']
            )
        )
        if not notes == '':
            updates['notes'] = notes
        
        ### Update the entry
        ### First open our normal csv file
        f = open(self.file_name, 'r')
        ### Than open a temporary one
        tempfile = open('temp.csv', 'w')
        ### Create writer and reader
        reader = DictReader(f, fieldnames=self.field_names)
        writer = DictWriter(tempfile, fieldnames=self.field_names)

        ### Copy each row to the temp file
        for row in reader:
            ### Edit the row we want to edit
            if reader.line_num == index:
                row.update(**updates)
            writer.writerow(dict(row))
        ### Close files
        tempfile.close()
        f.close()

        ### Replace our normal file with the contents of the edited file
        ### And remove the edited file
        ### This because we can't edit a file in place  
        shutil.move(tempfile.name, self.file_name)
        print('Updated entry!')
