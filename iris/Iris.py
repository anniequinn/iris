import re
import numpy as np

from iris.ColourSpace import (
    HexColourSpace,
    RGBColourSpace,
    LabColourSpace,
    XYZColourSpace,
)


class Iris:
    RE_PATTERNS = {
        "hex": [r"^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"],
        "rgb": [
            r"^rgb\(\s*(-?\d+),\s*(-?\d+)\s*,\s*(-?\d+)\s*\)$",
            r"r=([0-9]+),g=([0-9]+),b=([0-9]+)",
        ],
        "lab": [
            r"^lab\(\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\s*\)$",
            r"^l=(-?\d+(?:\.\d+)?),a=(-?\d+(?:\.\d+)?),b=(-?\d+(?:\.\d+)?)$",
        ],
        "xyz": [
            r"^xyz\(\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\s*\)$",
            r"^x=(-?\d+(?:\.\d+)?),y=(-?\d+(?:\.\d+)?),z=(-?\d+(?:\.\d+)?)$",
        ],
    }

    def __init__(self, user_input):
        # NOTE re user_input
        # - Do not separate colours with a comma
        # - Spaces outside of brackets means a new colour
        self.user_input = user_input
        self.validate_input()

        self.colour_strs = []
        self.colour_spaces = []
        self.iris_colours = []
        self.iris_colour_space = None

        self.preprocess_colours()

    def validate_input(self):
        if not isinstance(self.user_input, str):
            raise ValueError("Input must be a str")

    def input_str_to_colour_list(self):
        return re.split(r";\s*|\s+(?![^\(\)]*\))", self.user_input)

    def identify_colour_space(self, colour_str):
        for space, patterns in Iris.RE_PATTERNS.items():
            for pattern in patterns:
                if re.match(pattern, colour_str):
                    return space

    def to_iris_colour(self, colour_space, colour_str):
        if colour_space == "hex":
            return HexColourSpace.to_iris_colour(colour_str)

        elif colour_space == "rgb":
            return RGBColourSpace.to_iris_colour(colour_str)

        elif colour_space == "lab":
            return LabColourSpace.to_iris_colour(colour_str)

        elif colour_space == "xyz":
            return XYZColourSpace.to_iris_colour(colour_str)

    def preprocess_single_colour(self, colour_str):
        colour_space = self.identify_colour_space(colour_str)
        self.colour_spaces.append(colour_space)
        iris_colour = self.to_iris_colour(colour_space, colour_str)
        self.iris_colours.append(iris_colour)

    def preprocess_colours(self):
        self.colour_strs = self.input_str_to_colour_list()

        for colour_str in self.colour_strs:
            self.preprocess_single_colour(colour_str)

        if len(set(self.colour_spaces)) > 1:
            raise ValueError("All colours must be in the same colour space")
        else:
            self.iris_colour_space = self.colour_spaces[0]
        # NOTE: Conversion will be added at a later date, including default colour space

        if self.iris_colour_space != "hex":
            self.iris_colours = np.array(self.iris_colours)
