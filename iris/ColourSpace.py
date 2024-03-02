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
        return hex_str

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
        return colour_arr

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
        return colour_arr

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
        return colour_arr

    @staticmethod
    def to_colour_space(xyz_arr, colour_space):
        """Convert XYZ array to another colour space."""
        if colour_space == "hex":
            return Converter.rgb2hex(Converter.xyz2rgb(xyz_arr))
        elif colour_space == "rgb":
            return Converter.xyz2rgb(xyz_arr)
        elif colour_space == "lab":
            return Converter.xyz2lab(xyz_arr)
