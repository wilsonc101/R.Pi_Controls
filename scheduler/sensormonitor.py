import time
import pycurl
from io import BytesIO

from subprocess import check_output

import core.Adafruit_MAX31855.MAX31855 as MAX31855
import core.redisdb as redisdb
import core.config as config
import core.sqlitedb as sqlitedb

class SensorMonitor():
    def __init__(self, logfile):
        self.logfile = logfile

        self.thermo_external_reading = None
        self.thermo_internal_reading = None
        self.uptime = None
        self.cpu_temp = None

        # Setup SQLite Connection - db name and path is fixed
        sqlitedb.initilise()
        self._db_check = False

        # Setup sensors/common items
        self.initilise_sensors()

        # AWS data template
        self._template = {'date': None,
                          'purge': None,
                          'data': None}


    def _post_aws_data(self, data):
        header = 'Content-Type:application/json'
        buffer = BytesIO()
        c = pycurl.Curl()
        try:
            c.setopt(c.URL, config.content.aws['post_url'])
            c.setopt(c.HTTPHEADER,[header])
            c.setopt(c.WRITEDATA, buffer)
            c.setopt(c.POSTFIELDS, str(data))
            c.perform()
            c.close()

            self.logfile.debug("AWS Posted - " + buffer.getvalue().decode('iso-8859-1'))
            return True

        except:
            self.logfile.warning("Failed to post to AWS")
            return False


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
            external_reading = None
            internal_reading = None
            while external_reading is None or internal_reading is None:
                external_reading = self.temp_sensor.readTempC()
                internal_reading = self.temp_sensor.readInternalC()

                # hold in loop if temp data ia bad
                if str(external_reading) == "nan" or str(internal_reading) == "nan":
                    external_reading = None
                    internal_reading = None
                    time.sleep(0.1)

            self.thermo_external_reading = "{0:0.2F}'C".format(external_reading)
            self.thermo_internal_reading = "{0:0.2F}'C".format(internal_reading)

            self.logfile.debug("Writing sensor data to store")
            redisdb.setObject("sensor_1", self.pi_cpu_temp)
            redisdb.setObject("sensor_2", self.thermo_internal_reading)
            redisdb.setObject("sensor_3", self.thermo_external_reading)
            redisdb.setObject("sensor_4", self.uptime)


            # Write timestamped TC sensor data to DB and prune data once every 5 mins
            time_mins = int(time.strftime("%M"))
            time_hours = int(time.strftime("%H"))
            time_now = time.strftime("%Y-%m-%dT%H:%M:%S")
            if time_mins % 5 == 0:
                if self._db_check is False:
                    self._db_check = True

                    sqlitedb.insert_sensor_data((self.thermo_internal_reading, 
                                                 self.thermo_external_reading, 
                                                 time_now))
                    self.logfile.info("Logging date to DB")

                    sqlitedb.prune_records()
                    self.logfile.info("Pruning date from DB")

                    # Post AWS data 20mins past the hour
                    if time_mins == 30:
                        data = self._template
                        data['date'] = time_now
                        data['data'] = [{'Name':'TC_External',
                                         'Value':str(external_reading)},
                                        {'Name':'TC_Internal',
                                         'Value':str(internal_reading)}]

                        # Trigger data purge at 2020hrs
                        if time_hours == 20:
                            data['purge'] = "True"
                        else:
                            data['purge'] = "False"

                        self._post_aws_data(data)

            # Reset db_check - ensures we only get one value every 5mins
            if time_mins % 5 > 0:
                self._db_check = False

            # Slow the loop to avoid thrashing the CPU
            time.sleep(2)

