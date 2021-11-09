import sys

from scanner import Scanner
from analyzer import Parser
from utils import printter

file_path = sys.argv[1]
scanner = Scanner(file_path)
scanner.scan()
tokens = scanner.printter()
parser = Parser(scanner.tokens)
parser.parse()
matches, symtable, errors = parser.printter()

printter(
    [
        {'name': 'VETOR DE TOKENS', 'content': tokens},
        {'name': 'SEQUÊNCIA DE COMPILAÇÃO', 'content': matches},
        {'name': 'TABELA DE SIMBOLOS', 'content': symtable},
        {'name': 'ERROS', 'content': errors}
    ], 
    file_path
)