import sys

from scanner import Scanner
from emulator import Parser

file_path = sys.argv[1]
scanner = Scanner(file_path)
scanner.scan()
parser = Parser(scanner.tokens)
parser.parse()