import webbrowser
import sys

request = "https://dreampuf.github.io/GraphvizOnline/#"

with open(sys.argv[1], 'r') as file:
  request += file.read()

webbrowser.open(request, new=2)