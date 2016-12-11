import time

import sqlite3
import pygal
from pygal.style import LightStyle


def _generate_graph(data, labels, output_file):
    line_chart = pygal.Line(width=400, height=250,
                            style=LightStyle,
                            show_legend=False,
                            x_label_rotation=20)

    line_chart.add('', data)
    line_chart.x_labels = labels
    line_chart.render_to_file(output_file)

    return True
    

def _get_db_data(db_cursor, sensor, table="sensor_data", date_column="record_date"):

    db_data = db_cur.execute("SELECT " + sensor_name + "," + date_column + \
                             " FROM " + table + \
                             " ORDER BY date(" + date_column +")")

    return db_data


if __name__ == "__main__":
    db_conn = sqlite3.connect('db/pi_control.db')
    db_cur = db_conn.cursor()

    sensor_name = "TC_external"
    graph_file = "webserver/images/" + sensor_name + "_graph.svg"


    data = _get_db_data(db_cur, sensor_name)

    formatted_data = list()
    label_data = list()

    count = 0
    for i in data:
        formatted_data.append(float(i[0].split("'")[0]))
        label_data.append(i[1].replace("T", " "))
        count = count + 1


    _generate_graph(formatted_data, label_data, graph_file)
    print("lines processed - " + str(count))





    

