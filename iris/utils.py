import re


class Utils:
    """Project-wide utility methods."""

    RE_PATTERNS = {
        "hex": r"^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        "rgb": r"^rgb\(\s*(-?\d+),\s*(-?\d+)\s*,\s*(-?\d+)\s*\)$",
        "hsl": r"^hsl\(\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)%\s*,\s*(-?\d+(?:\.\d+)?)%\s*\)$",  # noqa
    }

    @staticmethod
    def input_is_str(input_str):
        """Confirm that `input_str` is a string."""
        if not isinstance(input_str, str):
            raise ValueError("Input `input_str` must be a string.")
        return True

    @staticmethod
    def identify_col_space(col_str):
        """Identify the colour space of `col_str` using regex patterns."""
        for space, pattern in Utils.RE_PATTERNS.items():
            if re.match(pattern, col_str):
                return space

        raise ValueError(
            f"Invalid colour space. Must be one of {', '.join(Utils.RE_PATTERNS.keys())}"  # noqa
        )

    @staticmethod
    def col_arr2str(col_arr, col_space):
        """Convert a colour array to a string."""
        if col_space not in Utils.RE_PATTERNS:
            raise ValueError(
                f"Invalid colour space. Must be one of {', '.join(Utils.RE_PATTERNS.keys())}"  # noqa
            )

        return f"{col_space}({', '.join(map(str, col_arr))})"
        # TODO: This shouldn't work for hex
