from datetime import datetime

from src.sundata import (
    LightPeriod,
    Position,
    get_lighting_period_after,
    get_lighting_period_before,
)


def test_get_night_before_date():
    pos = Position(51.772938, 0.102310)
    sunrise = datetime(2023, 2, 12, 8, 3)
    night_end = get_lighting_period_before(pos, sunrise, LightPeriod.NIGHT)
    assert night_end == datetime(2023, 2, 12, 5, 26)


def test_get_nght_after_date():
    pos = Position(51.772938, 0.102310)
    sunset = datetime(2023, 2, 12, 17, 7)
    night_start = get_lighting_period_after(pos, sunset, LightPeriod.NIGHT)
    assert night_start == datetime(2023, 2, 12, 19, 2)
