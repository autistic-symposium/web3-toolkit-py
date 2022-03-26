import pytz
import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


def _find_timezone(lat, lon) -> int:
    obj = TimezoneFinder()
    tzone = obj.timezone_at(lng=lon, lat=lat)
    timezone = datetime.datetime.now(pytz.timezone(tzone)).strftime('%z')
    try:
        timezone = int(timezone[:-2])
    except:
        print('Error formatting timezone {}'.format(timezone))
    return timezone


def get_location(data) -> dict:
    try:
        city = data['city']
    except:
        print('Data is ill-formatted: {}'.format(data))

    geolocator = Nominatim(user_agent="$choices")
    location = geolocator.geocode(city)

    data = {
        'lat': location.latitude,
        'lon': location.longitude,
        'tzone': _find_timezone(location.latitude, location.longitude)
    }

    return data


