import time
import sqlite3

from subprocess import check_output

import core.Adafruit_MAX31855.MAX31855 as MAX31855
import core.redisdb as redisdb


class SensorMonitor():
    def __init__(self, logfile):
        self.logfile = logfile

        self.thermo_external_reading = None
        self.thermo_internal_reading = None
        self.uptime = None
        self.cpu_temp = None

        # Setup SQLite Connection
        self.db_conn = sqlite3.connect('db/pi_control.db')
        self.db_cur = self.db_conn.cursor()
        self.db_cur.execute("CREATE TABLE IF NOT EXISTS sensor_data (TC_internal, TC_external)")

        self.temp_data_sql = "INSERT INTO sensor_data(TC_internal, TC_external) VALUES(?, ?) "
        self._db_check = False

        # Setup sensors/common items
        self.initilise_sensors()


    def initilise_sensors(self):
        # Setup thermo-couple reader NAX31855 on SPI
        CLK = 25
        CS = 24
        DO = 18
        self.temp_sensor = MAX31855.MAX31855(CLK, CS, DO)

        self.cmd_uptime = ["/usr/bin/uptime", "-p"]
        self.cmd_cpu_temp = ["/opt/vc/bin/vcgencmd", "measure_temp"]

        self.logfile.info("Sensors init - success")


    def run_schedule(self):
        while True:
            # Get CPU Temp (C)
            self.pi_cpu_temp = check_output(self.cmd_cpu_temp).decode("utf-8").replace("temp=", "")

            # Get system uptime
            self.uptime = check_output(self.cmd_uptime).decode("utf-8").lstrip().replace("up ", "").replace(", ", "\n")

            # Get thermocouple Temps (C)
            while self.thermo_external_reading == None and self.thermo_internal_reading == None:
                external_reading = self.temp_sensor.readTempC()
                internal_reading = self.temp_sensor.readInternalC()
                time.sleep(0.1)

                # filter out bad data
                if str(external_reading) != "nan" and str(internal_reading) != "nan":
                    self.thermo_external_reading = "{0:0.2F}'C".format(external_reading)
                    self.thermo_internal_reading = "{0:0.2F}'C".format(internal_reading)

            self.logfile.debug("Writing sensor data")
            redisdb.setObject("sensor_1", self.pi_cpu_temp)
            redisdb.setObject("sensor_2", self.thermo_internal_reading)
            redisdb.setObject("sensor_3", self.thermo_external_reading)
            redisdb.setObject("sensor_4", self.uptime)

            # Write TC sensor data to DB every 5 mins
            time_mins = int(time.strftime("%M"))
            if time_mins % 5 == 0 and not self._db_check:
                self.db_cur.execute(self.temp_data_sql, (self.thermo_internal_reading, self.thermo_external_reading))
                self.db_conn.commit()
                self._db_check = True

            # Reset db_check - ensures we only get one value every 5mins
            if time_mins % 5 > 0:
                self.db_check = False
                
            time.sleep(1)


