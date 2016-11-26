import time

from subprocess import check_output

import core.Adafruit_GPIO.SPI as SPI
import core.Adafruit_MAX31855.MAX31855 as MAX31855

# Setup thermo-couple reader NAX31855 on SPI
CLK = 25
CS  = 24
DO  = 18
sensor = MAX31855.MAX31855(CLK, CS, DO)

def get_sensor_data():
    data = dict()

    # Get CPU Temp (C)
    pi_cpu_temp = str(check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]).rstrip()).split("=")[1].split('"')[0]

    # Get thermocouple Temps (C)
    thermo_external_reading = None
    thermo_internal_reading = None
    while thermo_external_reading == None and thermo_internal_reading == None:
#        external_reading = sensor.readTempC()     #    Real sensor disabled
        external_reading = 0.0
        internal_reading = sensor.readInternalC()

        # filter out bad data
        if str(external_reading) != "nan" and str(internal_reading) != "nan":
            thermo_external_reading = str(external_reading) + "'C"
            thermo_internal_reading = str(internal_reading) + "'C"

        time.sleep(0.1)

    data["sensor_1"] = pi_cpu_temp
    data["sensor_2"] = thermo_internal_reading
    data["sensor_3"] = thermo_external_reading
    data["sensor_4"] = "four"

    return data
