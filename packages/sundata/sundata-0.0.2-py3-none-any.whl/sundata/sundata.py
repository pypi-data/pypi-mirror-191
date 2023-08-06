from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

import astropy.coordinates as coord
import astropy.units as u
import pytz
from astropy.time import Time
from suntime import Sun


@dataclass
class Position:
    latitude: float
    longitude: float


class LightPeriod(Enum):
    NIGHT = 0
    ASTRO = 1
    NAUTICAL = 2
    CIVIL = 3
    DAY = 4


class LightingInformation:
    sunrise: datetime
    sunset: datetime
    location: Position
    set_date: datetime
    utc = pytz.UTC

    def __init__(self, position: Position, a_datetime: datetime) -> None:
        self.location = position
        self.set_date = a_datetime.astimezone(self.utc)

    def calculate(self, lighting_period: LightPeriod = LightPeriod.DAY):
        sun = Sun(self.location.latitude, self.location.longitude)
        self.sunrise = sun.get_local_sunrise_time(self.set_date).astimezone(self.utc)
        sunrise_angle = get_sun_altitude(self.location, self.sunrise)
        if sunrise_angle < 0 and lighting_period == LightPeriod.DAY:
            self.sunrise = get_lighting_period_after(
                self.location, self.sunrise, lighting_period
            )
        else:
            self.sunrise = get_lighting_period_before(
                self.location, self.sunrise, lighting_period
            )

        self.sunset = sun.get_local_sunset_time(self.set_date).astimezone(self.utc)
        sunset_angle = get_sun_altitude(self.location, self.sunset)

        if sunset_angle < 0 and lighting_period == LightPeriod.DAY:
            self.sunset = get_lighting_period_before(
                self.location, self.sunset, lighting_period
            )
        else:
            self.sunset = get_lighting_period_after(
                self.location, self.sunset, lighting_period
            )


def get_sun_altitude(position: Position, when: datetime) -> float:
    earth_location = coord.EarthLocation(
        lon=position.longitude * u.deg, lat=position.latitude * u.deg
    )
    when = Time(when, format="datetime", scale="utc")
    altazframe = coord.AltAz(obstime=when, location=earth_location)
    sunaltaz = coord.get_sun(when).transform_to(altazframe)
    return sunaltaz.alt.max().value


def lighting_is(sun_altitude: float) -> LightPeriod:
    if sun_altitude >= 0:
        return LightPeriod.DAY
    if sun_altitude < -18:
        return LightPeriod.NIGHT
    if sun_altitude < 0 and sun_altitude >= -6:
        return LightPeriod.CIVIL
    if sun_altitude < -6 and sun_altitude >= -12:
        return LightPeriod.NAUTICAL
    if sun_altitude < -12 and sun_altitude >= -18:
        return LightPeriod.ASTRO


def get_lighting_period_after(
    position: Position, when: datetime, period: LightPeriod
) -> datetime:
    lighting = when

    while period.value != lighting_is(get_sun_altitude(position, lighting)).value:
        lighting = lighting + timedelta(minutes=1)

    return lighting


def get_lighting_period_before(
    position: Position, when: datetime, period: LightPeriod
) -> datetime:
    lighting = when

    while period.value != lighting_is(get_sun_altitude(position, lighting)).value:
        lighting = lighting - timedelta(minutes=1)

    return lighting
