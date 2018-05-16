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
        """Setup Search Model for use"""
        ### Clear screen
        clear()
        ### Get search option
        option = input(self.SEARCH_MENU)
        try:
            option = self.SEARCH_OPTIONS[int(option)]
        except ValueError:
            pass
        except KeyError:
            option = 'UNDEFINED'
        
        ### Check option
        option = option.upper()
        if option == 'Q':
            print('Returning to main menu')
            return None
        ### Get and set function + kwargs based on user input
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
        
        ### Get entries for user input
        return self.get_entries(func, **kwargs)
    
    def default_func(self, **kwargs):
        """Here as backup"""
        ### In theory, this should never get used, but just here
        ### In case something breaks it on accident
        print('Something went terribly wrong! Restarting program')
        return None

    def get_date_kwargs(self):
        """Get data for the date search option"""
        ### Get user input
        date = input('Please give a date in the format MM/DD/YYYY\t')
        ### Validate user input
        try:
            datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            print('Invalid date!')
            return self.get_date_kwargs()
        ### Return data
        return {'date': date}
    
    def entries_by_date(self, row, date):
        """Check if the row confirms to the date data"""
        if row['date'] == date:
            return True
        return False

    def get_time_spent_kwargs(self):
        """Get data for the time spent search option"""
        ### Get user input
        time_spent = input('Please give a time spent in minutes\t')
        ### Validate user input
        try:
            int(time_spent)
        except ValueError:
            print('Invalid time spent. Should be a number')
            return self.get_time_spent_kwargs()
        ### Return data
        return {'time': time_spent}
    
    def entries_by_time_spent(self, row, time):
        """Check if the row confirms to the time spent data"""
        if row['time'] == time:
            return True
        return False
    
    def get_exact_kwargs(self):
        """Get data for the exact search option"""
        ### Get user input
        searchable_fields = ['name', 'notes']
        field = input('Please give field name to filter on. Can be {}\t'.format(' or '.join(searchable_fields)))
        ### Validate input
        if not field in searchable_fields:
            print('Invalid field')
            return self.get_exact_kwargs()
        value = input('Please give a value to search for\t')
        ### Return data
        return {'field': field, 'value': value}
    
    def entries_by_exact_search(self, row, field, value):
        """Check if the row confirms to the exact search data"""
        if value in row[field]:
            return True
        return False
    
    def get_regex_kwargs(self):
        """Get data for the regex search option"""
        ### Get user input
        searchable_fields = ['name', 'notes']
        field = input('Please give field name to filter on. Can be {}\t'.format(' or '.join(searchable_fields)))
        ### Validate input
        if not field in searchable_fields:
            print('Invalid field')
            return self.get_regex_kwargs()
        regex = input('Please give me a string to use as regular expression\t')
        ### Return data
        return {'field': field, 'regex': regex}

    def entries_by_regex(self, row, field, regex):
        """Check if the row confirms to the regex data"""
        if re.search(r'{}'.format(regex), row[field], 'i'):
            return True
        return False

    def get_date_range_kwargs(self):
        """Get data for the date range search option"""
        ### Get user input
        start = input('Please give a start date in format MM/DD/YYYY\t')
        end = input('Please give an end date in format MM/DD/YYYY\t')
        ### Validate input
        try:
            start = datetime.strptime(start, '%m/%d/%Y').date()
            end = datetime.strptime(end, '%m/%d/%Y').date()
        except ValueError:
            print('Invalid date(s) provided!')
            return self.get_date_kwargs()
        ### Return data
        return {'start': start, 'end': end}
    
    def entries_by_date_range(self, row, start, end):
        """Check if the row confirms to the date range data"""
        date = datetime.strptime(row['date'], '%m/%d/%Y').date()
        if start <= date <= end:
            return True
        return False

    def get_entries(self, func, **kwargs):
        """Get entries for the search option/data the user entered"""
        ### Open file
        with open(self.file_name, 'r') as f:
            entries = []
            reader = DictReader(f, fieldnames=self.field_names)
            ### Check if we should keep the row
            ### Also adds row number to the dict that we need to edit the row
            for row in reader:
                row.update({'line': reader.line_num})
                if func(row, **kwargs):
                    entries.append(row)
            ### Return entries for the search query
            return entries
