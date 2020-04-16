import webbrowser
import sys
from urllib.parse import quote

request = r"https://dreampuf.github.io/GraphvizOnline/#"

filename = "generated_dot.txt"
if len(sys.argv) > 1:
    filename  = sys.argv[1]
file = open(filename , "r")
request += quote(file.read())
file.close()
webbrowser.open(request, new=2)


