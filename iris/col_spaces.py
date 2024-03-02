class HexColSpace:
    """Methods for working with the hex colour space."""

    @staticmethod
    def _rm_lead_hash(hex_str):
        """Remove leading hash from hex string."""
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
    def get_valid_hex_str(hex_str):
        """Return a valid hex string."""
        hex_str = HexColSpace._rm_lead_hash(hex_str)
        hex_str = HexColSpace._expand_short_notation(hex_str)
        return hex_str


class RGBColSpace:
    """Methods for working with the RGB colour space."""

    @staticmethod
    def _get_arr(col):
        """Extract RGB values from `col` and return as an array of integers."""
        match = re.findall(r"-?\d+", col)
        return np.array(match, dtype=int)

    @staticmethod
    def _clip_arr(col_arr):
        """Clip RGB values to valid range [0, 255]."""
        return np.clip(col_arr, 0, 255)

    @staticmethod
    def get_valid_col_arr(col):
        """Return a valid RGB array."""
        col_arr = RGBColSpace._get_arr(col)
        col_arr = RGBColSpace._clip_arr(col_arr)
        return col_arr


class HexRGB:
    """Methods for converting between hex and RGB colour spaces."""

    @staticmethod
    def hex2rgb(hex_str):
        """Convert hex string to RGB array."""
        return np.array([int(hex_str[i : i + 2], 16) for i in (0, 2, 4)])

    @staticmethod
    def rgb2hex(rgb_arr):
        """Convert RGB array to hex string."""
        # return "#{:02x}{:02x}{:02x}".format(*rgb_arr)
        return "#{:02x}{:02x}{:02x}".format(*map(int, rgb_arr))

    # TODO: Add error handling to HexRGB