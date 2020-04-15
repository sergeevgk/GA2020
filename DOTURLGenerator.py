import webbrowser
import sys
from urllib.parse import quote

request = r"https://dreampuf.github.io/GraphvizOnline/#"

file = open(sys.argv[1], "r")
request += quote(file.read())
file.close()
webbrowser.open(request, new=2)


