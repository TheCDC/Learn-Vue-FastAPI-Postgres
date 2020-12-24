legal_chars = "1234567890abcdefABCDEF"


def validate_color(s: str) -> bool:
    if not len(s) == 7:
        return False
    if not s[0] == "#":
        return False
    if not all(c in legal_chars for c in s[1:]):
        return False
    return True
