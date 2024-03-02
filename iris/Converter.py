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