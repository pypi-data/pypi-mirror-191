from datetime import datetime

import pytz

from src.sundata import LightingInformation, LightPeriod, Position

zone = pytz.UTC


def test_default_sunrise_sunset():
    position = Position(51.772938, 0.102310)
    a_date = datetime(2023, 2, 13, 12, 00)
    data = LightingInformation(position, a_date)
    data.calculate()
    assert data.sunrise == datetime(2023, 2, 13, 7, 25).astimezone(zone)
    assert data.sunset == datetime(2023, 2, 13, 17, 3).astimezone(zone)


def test_default_sunrise_sunset_DAYLIGHT():
    position = Position(51.772938, 0.102310)
    a_date = datetime(2023, 2, 13, 12, 00)
    data = LightingInformation(position, a_date)
    data.calculate()
    assert data.sunrise == datetime(2023, 2, 13, 7, 25).astimezone(zone)
    assert data.sunset == datetime(2023, 2, 13, 17, 3).astimezone(zone)


def test_default_sunrise_sunset_CIVIL():
    position = Position(51.772938, 0.102310)
    a_date = datetime(2023, 2, 13, 12, 00)
    data = LightingInformation(position, a_date)
    data.calculate(LightPeriod.CIVIL)
    assert data.sunrise == datetime(2023, 2, 13, 7, 19).astimezone(zone)
    assert data.sunset == datetime(2023, 2, 13, 17, 10).astimezone(zone)


def test_default_sunrise_sunset_():
    position = Position(51.772938, 0.102310)
    a_date = datetime(2023, 2, 13, 12, 00)
    data = LightingInformation(position, a_date)
    data.calculate(LightPeriod.NAUTICAL)
    assert data.sunrise == datetime(2023, 2, 13, 6, 43).astimezone(zone)
    assert data.sunset == datetime(2023, 2, 13, 17, 45).astimezone(zone)


def test_default_sunrise_sunset_():
    position = Position(51.772938, 0.102310)
    a_date = datetime(2023, 2, 13, 12, 00)
    data = LightingInformation(position, a_date)
    data.calculate(LightPeriod.ASTRO)
    assert data.sunrise == datetime(2023, 2, 13, 6, 4).astimezone(zone)
    assert data.sunset == datetime(2023, 2, 13, 18, 25).astimezone(zone)


def test_default_sunrise_sunset_():
    position = Position(51.772938, 0.102310)
    a_date = datetime(2023, 2, 13, 12, 00)
    data = LightingInformation(position, a_date)
    data.calculate(LightPeriod.NIGHT)
    assert data.sunrise == datetime(2023, 2, 13, 5, 25).astimezone(zone)
    assert data.sunset == datetime(2023, 2, 13, 19, 4).astimezone(zone)
