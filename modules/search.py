import re
from csv import DictReader
from datetime import datetime
from time import sleep

from modules.module import Module
from utils import clear, finalize


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
Or press \033[4mQ\033[0m to go back to the main menu]\n\n'''

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
            return None
        kwargs = {}
        func = self.default_func
        if option == 'C':
            kwargs = self.get_date_kwargs()
            func = self.entries_by_date
        elif option == 'T':
            kwargs = self.get_time_spent_kwargs()
            func = self.entries_by_time_spent
        elif option == 'E':
            kwargs = self.get_exact_kwargs()
            func = self.entries_by_exact_search
        elif option == 'R':
            kwargs = self.get_regex_kwargs()
            func = self.entries_by_regex
        elif option == 'D':
            kwargs = self.get_date_range_kwargs()
            func = self.entries_by_date_range
        else:
            print('Undefined option! Restarting!')
            sleep(1)
            self.setup()
        
        return self.get_entries(func, **kwargs)
    
    def default_func(self, **kwargs):
        print('Something went terribly wrong! Restarting program')
        return None

    def get_date_kwargs(self):
        date = input('Please give a date in the format MM/DD/YYYY\t')
        try:
            datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            print('Invalid date!')
            return self.get_date_kwargs()
        return {'date': date}
    
    def entries_by_date(self, reader, date):
        entries = []
        for row in reader:
            if row['date'] == date:
                entries.append(row)
        return entries

    def get_time_spent_kwargs(self):
        time_spent = input('Please give a time spent in minutes\t')
        try:
            int(time_spent)
        except ValueError:
            print('Invalid time spent. Should be a number')
            return self.get_time_spent_kwargs()
        return {'time': time_spent}
    
    def entries_by_time_spent(self, row, time):
        if row['time'] == time:
            return True
        return False
    
    def get_exact_kwargs(self):
        searchable_fields = ['name', 'notes']
        field = input('Please give field name to filter on. Can be {}\t'.format(' or '.join(searchable_fields)))
        if not field in searchable_fields:
            print('Invalid field')
            return self.get_exact_kwargs()
        value = input('Please give a value to search for\t')
        return {'field': field, 'value': value}
    
    def entries_by_exact_search(self, row, field, value):
        if row[field] == value:
            return True
        return False
    
    def get_regex_kwargs(self):
        searchable_fields = ['name', 'notes']
        field = input('Please give field name to filter on. Can be {}\t'.format(' or '.join(searchable_fields)))
        if not field in searchable_fields:
            print('Invalid field')
            return self.get_regex_kwargs()
        regex = input('Please give me a string to use as regular expression\t')
        return {'field': field, 'regex': regex}

    def entries_by_regex(self, row, field, regex):
        if re.search(r'{}'.format(regex), row[field]):
            return True
        return False

    def get_date_range_kwargs(self):
        start = input('Please give a start date in format MM/DD/YYYY\t')
        end = input('Please give an end date in format MM/DD/YYYY\t')
        try:
            start = datetime.strptime(start, '%m/%d/%Y').date()
            end = datetime.strptime(end, '%m/%d/%Y').date()
        except ValueError:
            print('Invalid date(s) provided!')
            return self.get_date_kwargs()
        return {'start': start, 'end': end}
    
    def entries_by_date_range(self, row, start, end):
        date = datetime.strptime(row['date'], '%m/%d/%Y').date()
        if start < date < end:
            return True
        return False

    def get_entries(self, func, **kwargs):
        with open(self.file_name, 'r') as f:
            entries = []
            reader = DictReader(f, fieldnames=self.field_names)
            for row in reader:
                if func(row, **kwargs):
                    entries.append(row)
            return entries
