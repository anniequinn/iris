import os; os.chdir(os.path.expanduser("~/git/personal/iris"))

import requests
import json
from bs4 import BeautifulSoup

from iris.ColourSpace import HexColourSpace

# Get colour names and hex codes from the W3C website
url = "https://www.w3.org/TR/css-color-3/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
colour_table = soup.find_all(class_="colortable")

w3cx11 = {}

for table in colour_table:
    colours = table.find_all("dfn")

    for colour in colours:
        # The colour name is the text within the <dfn> tag
        # The next <td> sibling contains the hex value
        colour_name = colour.get_text()
        hex_code = colour.find_next_sibling("td").get_text()
        hex_code = hex_code.split("\n\n")[0]

        w3cx11[colour_name] = hex_code

# Sort the dictionary by colour in the lab space
lab_w3cx11 = {}

for colour, hex_code in w3cx11.items():
    hex_code = HexColourSpace.to_iris_colour(hex_code)
    lab_w3cx11[colour] = HexColourSpace.to_colour_space(hex_code, "lab")

lab_w3cx11 = dict(sorted(lab_w3cx11.items(), key=lambda item: item[1][0]))

# Save the keys from lab and reorder the original hex codes
lab_keys = list(lab_w3cx11.keys())
w3cx11 = {k: w3cx11[k] for k in lab_keys}

# Save the dictionary to a JSON file
with open("data/w3cx11.json", "w") as file:
    json.dump(w3cx11, file, indent=4)
