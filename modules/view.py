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
            entry = self.entries[self.index]
            line = entry['line']
            self.update_row(line, entry)
        elif action == 'Q':
            return
        else:
            print('Invalid option. Restarting')
            sleep(1)
            self.load_entries()

    def update_row(self, index, row):
        clear()
        updates = {'date': datetime.utcnow().strftime('%m/%d/%Y')}
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
        
        f = open(self.file_name, 'r')
        tempfile = open('temp.csv', 'w')
        reader = DictReader(f, fieldnames=self.field_names)
        writer = DictWriter(tempfile, fieldnames=self.field_names)

        for row in reader:
            if reader.line_num == index:
                row.update(**updates)
            writer.writerow(dict(row))
        tempfile.close()
        f.close()
            
        shutil.move(tempfile.name, self.file_name)
        print('Updated entry!')
