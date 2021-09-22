import sys

from scanner import Scanner

file_path = sys.argv[1]
scanner = Scanner(file_path)
scanner.scan()
scanner.printter()