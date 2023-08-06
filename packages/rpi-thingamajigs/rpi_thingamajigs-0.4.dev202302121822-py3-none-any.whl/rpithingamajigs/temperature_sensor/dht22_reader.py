import logging
from datetime import datetime, timedelta
import threading
from time import sleep
import random
from rpithingamajigs.temperature_sensor import TemperatureSensor, Measurement


class DHT22Reader():
    """DHT22Reader reads from a physical DHT22 sensor and submits the data to the sensor object."""

    def __init__(self, iopin=None, sensor=None, simulate=False):
        self._logger = logging.getLogger('DHT22rdr')
        self._iopin = iopin
        self._sensor = sensor
        self._thread = None
        self._terminate = False
        self._simulate = simulate

    def log(self):
        return self._logger

    def _run(self):
        self.log().debug("Temperature reader thread started.")
        interval = 15
        spot = datetime.now()
        while True:
            # is the thread supposed to terminate?
            if self._terminate:
                self.log().debug("Termination requested. Quitting reader thread.")
                return
            # take a measurement:
            measurement = Measurement(spot)
            if self._simulate:
                humidity, temperature = self._simulate_read()
                measurement.humidity = humidity
                measurement.temperature = temperature
            else:
                humidity, temperature = self._dht22_read()
                measurement.humidity = humidity
                measurement.temperature = temperature
            if measurement.temperature != None and measurement.humidity != None:
                self.log().debug("Submitting measurement to sensor: {}.".format(measurement))
                self._sensor.add_measurement(measurement)
            else:
                self.log().warning("Invalid measurement reading. Continuing.")
            while True:
                spot = spot + timedelta(seconds=interval)
                delta = (spot - datetime.now()).total_seconds()  # how long is that from now?
                if delta > 0.25*interval:
                    self.log().debug("Next reading in {} seconds.".format(delta))
                    sleep(delta)
                    break
                self.log().debug("Adjusting to one skipped interval.")

    def start(self):
        self.log().info("Starting temperature reader thread.")
        self._thread = threading.Thread(target=self._run)
        self._thread.setName('DHT22Reader')
        self._thread.start()

    def quit(self):
        self.log().debug("Quitting DHT22 reader thread.")
        self._terminate = True

    def join(self):
        self.log().debug("Joining DHT22 reader thread...")
        self._thread.join()
        self.log().info("DHT22 reader thread has terminated...")

    def _dht22_read(self):
        """This function is separate so that the module can be simulated and tested without the sensor present."""
        import Adafruit_DHT  # pylint: disable=import-error
        self.log().debug("Reading temperature data from GPIO pin {}...".format(self._iopin))
        humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT22, self._iopin)
        if humidity is None or temperature is None:
            self.log().warning("Failure taking sensor read. Possible wiring issue.")
            return None, None
        self.log().debug("Temperature reading from sensor (raw data): {: .1f} / {: .1f}.".format(temperature, humidity))
        return 0.01*humidity, temperature

    def _simulate_read(self):
        self.log().debug("Simulating reading temperature data...")
        humidity = 0.5 + (0.9*random.random()-0.45)
        temperature = 10.0 + (60*random.random()-30)
        sleep(11.0*random.random())
        return humidity, temperature


# a simple demo:
if __name__ == "__main__":
    try:
        sensor = TemperatureSensor()
        # The dht22 object reads the temperature and humidity data and submits it to the sensor object.
        # Other components interact only with the sensor as a proxy.
        dht22 = DHT22Reader(4, sensor, simulate=True)
        # The reader object runs a thread thata treads the data in the background.
        dht22.start()
        for step in range(12):
            sleep(10)
            now = datetime.now()
            logging.debug("1min: {} - 5min: {} - 15min: {}".format(sensor.get_1min_average(now).temperature,
                                                                   sensor.get_5min_average(now).temperature, sensor.get_15min_average(now).temperature))
        logging.info("{} measurements collected. 1 minute average temperature is {}.".format(
            len(sensor.measurements()), sensor.get_15min_average(datetime.now()).temperature))
    finally:
        dht22.quit()
        dht22.join()
