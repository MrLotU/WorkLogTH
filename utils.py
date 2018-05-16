import os
import sys

def clear():
    """Clear the terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def finalize():
    """Provides a message to the user and cleanly exits the program"""
    print('\nShutting down. We hope to see you again!')
    sys.exit(0)
