import logging
from datetime import datetime, timedelta
from collections import deque
from threading import Lock

def _clamp(value, minvalue, maxvalue):
    if value < minvalue:
        return minvalue
    elif value > maxvalue:
        return maxvalue
    else:
        return value

class Measurement():
    def __init__(self, timestamp=None, temperature=None, humidity=None, datapoints=1):
        self._timestamp = timestamp
        self._temperature = temperature
        self._humidity = humidity
        self._datapoints = datapoints

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, t):
        self._timestamp = t

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature):
        self._temperature = temperature

    @property
    def humidity(self):
        return self._humidity 
    
    def humidity_bounded(self):
        """Returns the humidity bounded to the valid range [0.0-1.0] or None."""
        if self._humidity is None:
            return None
        return _clamp(self.humidity, 0.0, 1.00)

    @humidity.setter
    def humidity(self, humidity):
        self._humidity = humidity

    @property
    def datapoints(self):
        return self._datapoints

    @datapoints.setter
    def datapoints(self, datapoints):
        self._datapoints = datapoints

    def is_valid(self):
        return self.temperature is not None and self.humidity is not None

    def __str__(self):
        humidity = self.humidity_bounded()
        humiditystring="---.-"
        if humidity is not None:
            humiditystring="{:5.1F}".format(100*humidity)
        temperaturestring="+/- -.-"
        if self.temperature is not None:
            temperaturestring="{: 5.1F}".format(self.temperature)
        return "{} {}°C {}%".format(self.timestamp or "(invalid)", temperaturestring, humiditystring)

    def __repr__(self):
        return "{} ({})".format(self.__str__(), self.datapoints)

class TemperatureSensor():
    def __init__(self):
        self._logger = logging.getLogger('tempsens')
        self._measurements = deque(maxlen=int(60/15*20))  # up to 20min measurements at one every 15 seconds
        self._lock = Lock()

    def log(self):
        return self._logger

    def get_1min_average(self, timestamp):
        with self._lock:
            measurements = self._measurements_in_timespan(timestamp, 60)
            value = self._average_for_measurements(measurements)
            return value

    def get_5min_average(self, timestamp):
        with self._lock:
            measurements = self._measurements_in_timespan(timestamp, 5*60)
            value = self._average_for_measurements(measurements)
            return value

    def get_15min_average(self, timestamp):
        with self._lock:
            measurements = self._measurements_in_timespan(timestamp, 15*60)
            value = self._average_for_measurements(measurements)
            return value

    def measurements(self):
        with self._lock:
            return self._measurements

    def capacity(self):
        return self._measurements.maxlen

    def _measurements_in_timespan(self, start, maxage):
        end = start - timedelta(seconds=maxage)
        return list(filter(lambda x: x._timestamp <= start and x._timestamp > end, self._measurements))

    def _average_for_measurements(self, measurements):
        result = Measurement()
        if not measurements:
            return Measurement()

        count = len(measurements)
        result = Measurement(datapoints=0)
        for measurement in measurements:
            result.temperature = (result.temperature or 0.0) + (measurement.temperature or 0.0)
            result.humidity = (result.humidity or 0.0) + (measurement.humidity or 0.0)
            result.datapoints += measurement.datapoints
        result.timestamp = measurements[0].timestamp
        result.temperature = result.temperature/count
        result.humidity = result.humidity/count
        return result

    def add_measurement(self, measurement):
        with self._lock:
            self._measurements.append(measurement)
            self.log().debug("New measurement: {}".format(measurement))
