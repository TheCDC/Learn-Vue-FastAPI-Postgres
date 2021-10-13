from pydantic.color import Color


def convert_color(c: Color):
    return c.as_hex()
