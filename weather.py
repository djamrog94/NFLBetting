import pyowm
import pytz
from dateutil import parser


def get_weather(location, time):
    try:
        owm = pyowm.OWM('146743aaae7047891821a405d8fb55bb')
        # convert time from EST to GMT for OWM
        time = time
        old_game_time = parser.parse(time)
        old_zone = pytz.timezone('Etc/GMT')
        old_time = old_game_time.astimezone(old_zone)
        location_in = location
        fc = owm.three_hours_forecast(location_in + ',USA')
        # get forecast (GMT Time)
        game_forecast = fc.get_weather_at(old_time)
        temp = game_forecast.get_temperature('fahrenheit')
        time = game_forecast.get_reference_time(timeformat='date')
        status = game_forecast.get_detailed_status()
        wind = game_forecast.get_wind()
        # convert time back to EST
        new_zone = pytz.timezone('US/Eastern')
        date = time.astimezone(new_zone)
        new_date = date.strftime('%m/%d/%Y %H:%M:%S')
        return 'The Temperature is: {0} F. in {1} at this time: {2}. It is {3}, and the wind is {4} mph'.format(temp['temp'], location, new_date,status,wind['speed'])
    except:
        return 'Could not get weather'