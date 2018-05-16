from csv import DictReader, DictWriter
from datetime import datetime

from modules.module import Module
from utils import clear


class CreateModule(Module):
    """Module for creating new entries"""

    def setup(self):
        clear()
        name = input('Give a name for the entry:\t')
        time = input('How many minutes did you spend on this entry:\t')
        notes = input('Please give any other notes:\n')
        try:
            int(time)
        except ValueError:
            print('Invalid time spent. Should be a number')
            self.setup()
        self.create_entry(name=name, time=time, notes=notes)
        print('Created entry!')


    def create_entry(self, **kwargs):
        """Creates a new entry with provided kwargs"""
        ### Open file
        with open(self.file_name, 'a') as f:
            ### Create writer with fieldnames
            writer = DictWriter(f, fieldnames=self.field_names)
            ### Set date
            kwargs['date'] = datetime.utcnow().strftime('%m/%d/%Y')
            ### Write to file
            writer.writerow(kwargs)
