import importing
import writing
import plotting
import exporting
import sys

def do():
    importing.do()
    writing.do()
    plotting.do(sys.argv[1:])
    exporting.do()

do()
