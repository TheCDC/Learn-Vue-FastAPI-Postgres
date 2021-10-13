from app.schemas.bekpack.validators import validate_color


def test_validate_color():
    assert not validate_color("not a color")
    assert not validate_color("bekky")
    assert not validate_color("wegwegweg")
    assert not validate_color("")  # too short
    assert not validate_color("000000")  # missing #
    assert not validate_color("abcdef")  # missing #
    assert not validate_color("fghijkl")  # illegal chars
    assert not validate_color("wegwegweg")
    assert validate_color("#000000")
    assert validate_color("#FF0000")
    assert validate_color("#00FF00")
    assert validate_color("#0000FF")
