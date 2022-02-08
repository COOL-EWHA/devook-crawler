import re


def remove_escape(string):
    return re.sub(
        "\s+",
        " ",
        string,
    )
