from subprocess import check_output

def get_sensor_data():
    data = dict()

    # Get CPU Temp (C)
    sensor_1_value = str(check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]).rstrip()).split("=")[1].split('"')[0]

    data["sensor_1"] = sensor_1_value
    data["sensor_2"] = "two"
    data["sensor_3"] = "three"
    data["sensor_4"] = "four"

    return data

