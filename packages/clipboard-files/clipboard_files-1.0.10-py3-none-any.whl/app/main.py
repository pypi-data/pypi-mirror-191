import os
import json
import argparse
import pyperclip
from gui import choose_file

def main():
    # color codes for formatting text in the console
    BOLD = '\033[1m'
    RESET = '\033[0m'
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'

    # set up argument parser for command line arguments
    parser = argparse.ArgumentParser(description='A script for copying file contents to the clipboard.')
    parser.add_argument('--push', metavar='file_path', type=str, help='Add file path to .pf.config')
    parser.add_argument('--pop', metavar='file_path', type=str, help='Remove file path from .pf.config')
    parser.add_argument('--print', action='store_true', help='Print the file path selection instead of copying its contents')
    args = parser.parse_args()

    # set up file path for .pf.config
    pf_config_path = os.path.expanduser('~/.pf.config')

    # create .pf.config if it doesn't exist
    if not os.path.exists(pf_config_path):
        with open(pf_config_path, 'w'): pass

    # handle --push and --pop commands
    if args.push:
        if not os.path.isfile(args.push):
            print(f'{ERROR}File not found: {BOLD}{args.push}{RESET}')
            exit()
        with open(pf_config_path, 'a') as f:
            f.write(args.push + '\n')
        print(f'Added {BOLD}{args.push}{RESET} to {pf_config_path}')
        exit()
    elif args.pop:
        with open(pf_config_path, 'r') as f:
            lines = f.readlines()
        try:
            index = int(args.pop)
            if index < 0 or index >= len(lines):
                raise ValueError()
            file_path = lines[index].strip()
        except ValueError:
            try:
                lines.remove(args.pop + '\n')
            except ValueError:
                print(f'{ERROR}File path not found: {BOLD}{args.pop}{RESET}')
                exit()
            with open(pf_config_path, 'w') as f:
                for line in lines:
                    f.write(line)
            print(f'Removed {BOLD}{args.pop}{RESET} from {pf_config_path}')
            exit()
        else:
            with open(pf_config_path, 'w') as f:
                for i, line in enumerate(lines):
                    if i != index:
                        f.write(line)
            print(f'Removed {BOLD}{file_path}{RESET} from {pf_config_path}')
            exit()

    # read file paths from .pf.config or command line arguments
    if os.path.exists(pf_config_path):
        with open(pf_config_path, 'r') as f:
            file_paths = [line.strip() for line in f.readlines()]
    else:
        file_paths = []

    if not file_paths:
        print(f'{ERROR}No file paths found in {pf_config_path}{RESET}')
        exit()

    # add command line arguments to file_paths
    selection = None

    if len(file_paths) == 1:
        selection = file_paths[0]

    while selection is None:
        selection = choose_file("Choose a file to copy:", file_paths)

    # read contents of selected file and copy to clipboard
    try:
        with open(selection, 'r') as f:
            contents = f.read()
    except FileNotFoundError:
        print(f'{ERROR}File not found: {BOLD}{selection}{RESET}')
        exit()

    pyperclip.copy(contents)

    print(f'{SUCCESS}Contents of {BOLD}{selection}{RESET} copied to clipboard.{RESET}')

if __name__ == '__main__':
    main()
    