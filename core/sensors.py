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
#    pi_cpu_temp = str(check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]).rstrip()).split("=")[1].split('"')[0]
    pi_cpu_temp = check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]).decode("utf-8").replace("temp=", "")
#.split("=")[1].split('"')[0]

    # Get system uptime
#    uptime = str(check_output(["/usr/bin/uptime", "-p"]).rstrip()).split("'")[1].split("up")[1]
    uptime = check_output(["/usr/bin/uptime", "-p"]).decode("utf-8").lstrip().replace("up ", "").replace(", ", "\n")

    # Get thermocouple Temps (C)
    thermo_external_reading = None
    thermo_internal_reading = None
    while thermo_external_reading == None and thermo_internal_reading == None:
        external_reading = sensor.readTempC()     #    Real sensor disabled
        internal_reading = sensor.readInternalC()

        # filter out bad data
        if str(external_reading) != "nan" and str(internal_reading) != "nan":
            thermo_external_reading = "{0:0.2F}'C".format(external_reading)
            thermo_internal_reading = "{0:0.2F}'C".format(internal_reading)

        time.sleep(0.1)

    data["sensor_1"] = pi_cpu_temp
    data["sensor_2"] = thermo_internal_reading
    data["sensor_3"] = thermo_external_reading
    data["sensor_4"] = uptime

    return data

