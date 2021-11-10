import sys

from scanner import Scanner
from analyzer import Parser
from utils import printter

file_path = sys.argv[1]
scanner = Scanner(file_path)
scanner.scan()
tokens = scanner.printter()
parser = Parser(scanner.tokens, scanner.errors)
parser.parse()
matches, symtable, errors = parser.printter()

printter(
    [
        {'name': 'VETOR DE TOKENS', 'content': tokens},
        {'name': 'TABELA DE SIMBOLOS', 'content': symtable},
        {'name': 'ERROS', 'content': errors},
        {'name': 'SEQUÊNCIA DE COMPILAÇÃO', 'content': matches}
    ], 
    file_path
)