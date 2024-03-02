import re

import numpy as np


class Converter:
    """
    Methods for directly converting between colour spaces.
    
    NOTE: Expects iris format as input. Hex strings should be in the format 
    "#RRGGBB". For other colour spaces, they should be represented as a numpy
    array of appropriate dtype.
    """

    @staticmethod
    def hex2rgb(hex_str):
        """Convert hex string to RGB array."""
        return np.array([int(hex_str[i: i + 2], 16) for i in (0, 2, 4)])

    @staticmethod
    def rgb2hex(rgb_arr):
        """Convert RGB array to hex string."""
        # return "#{:02x}{:02x}{:02x}".format(*rgb_arr)
        return "#{:02x}{:02x}{:02x}".format(*map(int, rgb_arr))

    @staticmethod
    def rgb2xyz(rgb_arr):
        """Convert RGB array to XYZ array."""
        # Normalize RGB values
        rgb_arr = rgb_arr / 255.0

        # Apply gamma correction
        rgb_arr = np.where(
            rgb_arr > 0.04045,
            ((rgb_arr + 0.055) / 1.055) ** 2.4,
            rgb_arr / 12.92,
        )

        # RGB to XYZ conversion matrix
        xyz_matrix = np.array(
            [
                [0.4124564, 0.3575761, 0.1804375],
                [0.2126729, 0.7151522, 0.0721750],
                [0.0193339, 0.1191920, 0.9503041],
            ]
        )

        # Convert
        xyz_arr = np.dot(xyz_matrix, rgb_arr.T).T

        # Assume sRGB D65 standard illuminant
        xyz_arr = xyz_arr * 100
        return xyz_arr

    @staticmethod
    def xyz2rgb(xyz_arr):
        """Convert XYZ array to RGB array."""
        # Convert to 0-1 scale
        xyz_arr = xyz_arr / 100.0

        # XYZ to RGB conversion matrix
        rgb_matrix = np.array(
            [
                [3.2404542, -1.5371385, -0.4985314],
                [-0.9692660, 1.8760108, 0.0415560],
                [0.0556434, -0.2040259, 1.0572252],
            ]
        )

        # Convert
        rgb_arr = np.dot(rgb_matrix, xyz_arr.T).T

        # Apply gamma correction
        rgb_arr = np.where(
            rgb_arr > 0.0031308,
            1.055 * (rgb_arr ** (1 / 2.4)) - 0.055,
            12.92 * rgb_arr,
        )

        # Clip to valid range
        rgb_arr = np.clip(rgb_arr * 255, 0, 255)

        # Round and convert to int
        rgb_arr = np.round(rgb_arr).astype(int)

        return rgb_arr

    @staticmethod
    def xyz2lab(xyz_arr):
        """Convert XYZ array to CIELAB array."""
        # Normalize XYZ values
        xyz_arr = xyz_arr / np.array([95.047, 100.000, 108.883])

        # Apply the cube root function
        xyz_arr = np.where(
            xyz_arr > 0.008856,
            xyz_arr ** (1 / 3),
            (7.787 * xyz_arr) + (16 / 116),
        )

        # Calculate Lab values
        L = (116 * xyz_arr[1]) - 16
        a = 500 * (xyz_arr[0] - xyz_arr[1])
        b = 200 * (xyz_arr[1] - xyz_arr[2])
        return np.array([L, a, b])

    @staticmethod
    def lab2xyz(lab_arr):
        """Convert CIELAB array to XYZ array."""
        # Calculate intermediate values
        y = (lab_arr[0] + 16) / 116
        x = lab_arr[1] / 500 + y
        z = y - lab_arr[2] / 200

        # Apply the cube function
        x = np.where(x > 0.206893, x**3, (x - 16 / 116) / 7.787)
        y = np.where(y > 0.206893, y**3, (y - 16 / 116) / 7.787)
        z = np.where(z > 0.206893, z**3, (z - 16 / 116) / 7.787)

        # Unnormalize XYZ values
        return np.array([95.047 * x, 100.000 * y, 108.883 * z])


import re
import numpy as np

# TODO: Add a parent class called ColourSpace
# TODO: populate with the classes for HEX, RGB, add an XYZ and a LAB

from iris.Converter import Converter


class HexColourSpace:
    """Methods for working with the hex colour space."""

    @staticmethod
    def _rm_lead_hash(hex_str):
        """Remove leading hash from hex str."""
        if hex_str.startswith("#"):
            hex_str = hex_str[1:]
        return hex_str

    @staticmethod
    def _expand_short_notation(hex_str):
        """Expand short hex notation (length 3) to full length (length 6)."""
        if len(hex_str) == 3:
            hex_str = "".join([c * 2 for c in hex_str])
        return hex_str

    @staticmethod
    def to_iris_colour(hex_str):
        """Return a valid hex str."""
        hex_str = HexColourSpace._rm_lead_hash(hex_str)
        hex_str = HexColourSpace._expand_short_notation(hex_str)
        return MyClass(hex_str, "hex")

    @staticmethod
    def to_colour_space(hex_str, colour_space):
        """Convert hex string to another colour space."""
        if colour_space == "rgb":
            return Converter.hex2rgb(hex_str)
        elif colour_space == "xyz":
            return Converter.rgb2xyz(Converter.hex2rgb(hex_str))
        elif colour_space == "lab":
            return Converter.xyz2lab(
                Converter.rgb2xyz(Converter.hex2rgb(hex_str))
            )


class RGBColourSpace:
    """Methods for working with the RGB colour space."""

    @staticmethod
    def _get_arr(colour):
        """Extract RGB values and return as an array of integers."""
        match = re.findall(r"-?\d+", colour)
        return np.array(match, dtype=int)

    @staticmethod
    def _clip_arr(colour_arr):
        """Clip RGB values to valid range [0, 255]."""
        return np.clip(colour_arr, 0, 255)

    @staticmethod
    def to_iris_colour(colour):
        """Return a valid RGB array."""
        colour_arr = RGBColourSpace._get_arr(colour)
        colour_arr = RGBColourSpace._clip_arr(colour_arr)
        return MyClass(colour_arr, "rgb")

    @staticmethod
    def to_colour_space(rgb_arr, colour_space):
        """Convert RGB array to another colour space."""
        if colour_space == "hex":
            return Converter.rgb2hex(rgb_arr)
        elif colour_space == "xyz":
            return Converter.rgb2xyz(rgb_arr)
        elif colour_space == "lab":
            return Converter.xyz2lab(Converter.rgb2xyz(rgb_arr))


class LabColourSpace:
    """Methods for working with the CIELAB colour space."""

    @staticmethod
    def _get_arr(colour):
        """Extract LAB values and return as an array of floats."""
        match = re.findall(r"-?\d+(?:\.\d+)?", colour)
        return np.array(match, dtype=float)

    @staticmethod
    def _clip_arr(colour_arr):
        """Clip LAB values to valid range."""
        colour_arr[0] = np.clip(colour_arr[0], 0, 100)
        colour_arr[1:] = np.clip(colour_arr[1:], -128, 127)
        return colour_arr

    @staticmethod
    def to_iris_colour(colour):
        """Return a valid LAB array."""
        colour_arr = LabColourSpace._get_arr(colour)
        colour_arr = LabColourSpace._clip_arr(colour_arr)
        return MyClass(colour_arr, "lab")

    @staticmethod
    def to_colour_space(lab_arr, colour_space):
        """Convert LAB array to another colour space."""
        if colour_space == "hex":
            return Converter.rgb2hex(
                Converter.xyz2rgb(Converter.lab2xyz(lab_arr))
            )
        elif colour_space == "rgb":
            return Converter.xyz2rgb(Converter.lab2xyz(lab_arr))
        elif colour_space == "xyz":
            return Converter.lab2xyz(lab_arr)


class XYZColourSpace:
    """Methods for working with the XYZ colour space."""

    @staticmethod
    def _get_arr(colour):
        """Extract XYZ values and return as an array of floats."""
        match = re.findall(r"-?\d+(?:\.\d+)?", colour)
        return np.array(match, dtype=float)

    @staticmethod
    def _clip_arr(colour_arr):
        """Clip XYZ values to valid range."""
        colour_arr = np.clip(colour_arr, 0, 100)
        return colour_arr

    @staticmethod
    def to_iris_colour(colour):
        """Return a valid XYZ array."""
        colour_arr = XYZColourSpace._get_arr(colour)
        colour_arr = XYZColourSpace._clip_arr(colour_arr)
        return MyClass(colour_arr, "xyz")

    @staticmethod
    def to_colour_space(xyz_arr, colour_space):
        """Convert XYZ array to another colour space."""
        if colour_space == "hex":
            return Converter.rgb2hex(Converter.xyz2rgb(xyz_arr))
        elif colour_space == "rgb":
            return Converter.xyz2rgb(xyz_arr)
        elif colour_space == "lab":
            return Converter.xyz2lab(xyz_arr)


class MyClass:
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

    def __init__(self, colour_input, colour_space=None):
        self.iris_colour = None
        self.iris_colour_space = None
        self.colour = None

        self.process_input(colour_input, colour_space)

    def process_input(self, colour_input, colour_space):
        """
        Process the input, setting the colour string as well as the colour and
        colour space in Iris format.
        """
        if isinstance(colour_input, str):
            self._process_string(colour_input)

        elif isinstance(colour_input, list):
            self._process_list(colour_input, colour_space)

        elif isinstance(colour_input, np.ndarray):
            self._process_array(colour_input, colour_space)

        else:
            raise ValueError("Unknown input type, boom")

    def _process_string(self, colour_input):
        """
        Process a string input, identifying the colour space and converting the
        string to an Iris colour format.
        """
        self.colour = colour_input
        self.iris_colour_space = self._identify_colour_space(colour_input)
        self.iris_colour = self._to_iris_colour(
            self.iris_colour_space, colour_input
        )

    def _process_list(self, colour_input, colour_space):
        self._process_array(np.array(colour_input), colour_space)

    def _process_array(self, colour_input, colour_space):
        if not colour_space:
            raise ValueError(
                "Must specify colour space if using a list or array input"
            )
        if colour_space not in self.RE_PATTERNS:
            raise ValueError("Unknown colour space")

        self.colour = f"{colour_space}({','.join([str(i) for i in colour_input])})"  # noqa
        self.iris_colour_space = colour_space
        self.iris_colour = colour_input

    def _identify_colour_space(self, colour_str):
        """Use regular expressions to identify the colour space."""
        for space, patterns in self.RE_PATTERNS.items():
            for pattern in patterns:
                if re.match(pattern, colour_str):
                    return space

    def _to_iris_colour(self, colour_space, colour_str):
        """Convert the input string to an Iris colour format."""
        if colour_space == "hex":
            return HexColourSpace.to_iris_colour(colour_str)

        elif colour_space == "rgb":
            return RGBColourSpace.to_iris_colour(colour_str)

        elif colour_space == "lab":
            return LabColourSpace.to_iris_colour(colour_str)

        elif colour_space == "xyz":
            return XYZColourSpace.to_iris_colour(colour_str)

    def __str__(self):
        return str(self.colour)

    def __repr__(self):
        return self.__str__()


nice_colour = MyClass("#FF0000")


def check_MyClass(colour_input):
    if isinstance(colour_input, MyClass):
        return colour_input
    else:
        try:
            return MyClass(colour_input)
        except ValueError as e:
            raise ValueError(f"Could not convert input to MyClass: {e}")


def handle_colour_collection(func):
    """This is a decorator to handle the case where the input is a ColourCollection."""

    def wrapper(colour_input, *args, **kwargs):
        if isinstance(colour_input, ColourCollection):
            # If the input is a ColourCollection, apply func to each colour in the collection
            return ColourCollection(
                [
                    func(colour, *args, **kwargs)
                    for colour in colour_input.colours
                ]
            )
        else:
            # Otherwise, just apply func to the input directly
            return func(colour_input, *args, **kwargs)

    return wrapper


@handle_colour_collection
def convert_colour(colour, new_colour_space):
    colour = check_MyClass(colour)

    if colour.iris_colour_space == "hex":
        output = HexColourSpace.to_colour_space(
            colour.iris_colour, new_colour_space
        )
        return MyClass(output, new_colour_space)

    elif colour.iris_colour_space == "rgb":
        output = RGBColourSpace.to_colour_space(
            colour.iris_colour, new_colour_space
        )
        return MyClass(output, new_colour_space)

    elif colour.iris_colour_space == "lab":
        output = LabColourSpace.to_colour_space(
            colour.iris_colour, new_colour_space
        )
        return MyClass(output, new_colour_space)

    elif colour.iris_colour_space == "xyz":
        output = XYZColourSpace.to_colour_space(
            colour.iris_colour, new_colour_space
        )
        return MyClass(output, new_colour_space)

    # TODO: The return of MyClass can probably happen within the ColourSpace classes


class ColourCollection:
    def __init__(self, colours):
        self.colours = [check_MyClass(colour) for colour in colours]
        self._confirm_colour_space()

    def _confirm_colour_space(self):
        iris_colour_space = self.colours[0].iris_colour_space
        self.colours = [
            (
                colour
                if colour.iris_colour_space == iris_colour_space
                else convert_colour(colour, iris_colour_space)
            )
            for colour in self.colours
        ]

    def add_colour(self, colour):
        self.colours.append(check_MyClass(colour))
        self._confirm_colour_space()

    def __str__(self):
        return str([str(colour) for colour in self.colours])

    def __repr__(self):
        return self.__str__()


# Test implementations below
new_colour = convert_colour(nice_colour, "rgb")

convert_colour("#FF0000", "rgb")
convert_colour("#FF0000", "lab")


col_collection = ColourCollection(["#FF0000", "#00FF00", "rgb(0,255,0)"])
col_collection.add_colour("#0000FF")
col_collection.add_colour("lab(0,0,0)")
col_collection

convert_colour(col_collection, "rgb")
