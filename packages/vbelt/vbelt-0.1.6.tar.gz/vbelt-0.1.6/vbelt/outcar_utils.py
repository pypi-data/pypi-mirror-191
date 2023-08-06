def get_species(file):
    sp = get_val(file, "VRHFIN", after=":", expect_equal=True)
    return sp if sp != "r" else "Zr"


def get_array(file, before, after=None, map_=None, delimiter=None, expect_equal=False):
    """ Find an array of values separated by whitespaces or delimiter

    :param file: source file
    :param before: a string to be found before the value on the same line
    :param after: (optional, None) a string to be found after the value on the same line or None.
    :param delimiter: (optional, None) a string separating the values or None
      None means that any sequence of whitespaces is consider a delimiter (see str.split)
    :param map_: (optional, None) called on each value if not None. If None, the strip method is called on each value
    :param expect_equal: (optional, False) if True, expect to find a '=' between before and the value
    :return: a number or None if not found
    """

    chunk = _get_val(file, before, after=after, expect_equal=expect_equal)

    if not chunk:
        return None

    lst = chunk.split(delimiter)

    return [map_(e) if map_ else e.strip() for e in lst]


def get_val(file, before, after=None, expect_equal=False, strip=True):
    """ Find a value in a list of string.

    :param file: source file
    :param before: a string to be found before the value on the same line
    :param after: (optional, None) a string to be found after the value on the same line or None.
      Only useful if the value is not followed by some sort of whitespaces
    :param expect_equal: (optional, False) if True, expect to find a '=' between before and the value
    :param strip: (optional, True) strip blansk around to value
    :return: a number or None if not found
    """

    chunk = _get_val(file, before, after=after, expect_equal=expect_equal)

    if not chunk:
        return None

    return chunk.strip() if strip else chunk


def get_float(file, before, after=None, expect_equal=False):
    v = _get_val(file, before, after=after, expect_equal=expect_equal)

    if v is None:
        return None

    try:
        return float(v)
    except ValueError:
        return None


def get_int(file, before, after=None, expect_equal=False):
    v = _get_val(file, before, after=after, expect_equal=expect_equal)

    if v is None:
        return None

    try:
        return int(v)
    except ValueError:
        return None


def _get_val(file, before, after=None, expect_equal=False):
    """ Find a value in a list of string.

    :param file: source file
    :param before: a string to be found before the value on the same line
    :param after: (optional, None) a string to be found after the value on the same line or None.
      Only useful if the value is not followed by some sort of whitespaces
    :param expect_equal: (optional, False) if True, expect to find a '=' between before and the value
    :return: a number or None if not found
    """

    for line in file:
        if before in line:
            chunk = line[line.index(before) + len(before):]

            if after:
                if after in chunk:
                    chunk = chunk[:chunk.index(after)]
                else:
                    continue

            if expect_equal:
                if '=' in chunk:
                    chunk = chunk[chunk.index('=') + 1:]
                else:
                    continue

            if not chunk.isspace():
                break
    else:  # if no break => if before and after not found
        return None

    return chunk
