from csv import DictWriter, DictReader
from modules.module import Module
from datetime import datetime

class CreateModule(Module):
    """Module for creating new entries"""

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
