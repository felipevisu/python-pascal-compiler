import sys

from scanner import Scanner
from analyzer import Parser

file_path = sys.argv[1]
scanner = Scanner(file_path)
scanner.scan()
scanner.printter()
parser = Parser(scanner.tokens)
parser.parse()