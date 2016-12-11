import time

import sqlite3
import pygal
from pygal.style import LightStyle

import core.config as config

# Database is in a fixed location relative to installation path
DB_CONN = sqlite3.connect(config.local_path + '/db/pi_control.db')
DB_CUR = DB_CONN.cursor()


def _generate_graph(data, labels, graph_title=""):

    # Use subdivision of data length for major points
    label_count = int(len(data)/10)

    # Format graph
    line_chart = pygal.Line(width=400, height=250,
                            style=LightStyle,
                            show_legend=False,
                            x_label_rotation=90,
                            x_labels_major_count=label_count,
                            show_minor_y_labels=True,
                            show_minor_x_labels=False,
                            show_only_major_dots=True,
                            dots_size=3,
                            title=graph_title)

    line_chart.add('', data)
    line_chart.x_labels = labels

    return line_chart.render_data_uri()
    

def render_sensor_data(sensor, db_cursor=DB_CUR, table="sensor_data", date_column="record_date"):

    # Get SQL data
    db_data = db_cursor.execute("SELECT " + sensor + "," + date_column + \
                                " FROM " + table + \
                                " ORDER BY date(" + date_column + ")" + \
                                " BETWEEN datetime('now','-1 day') AND datetime('now')")

    # Loop SQL data and format for graphing
    formatted_data = list()
    label_data = list()

    for i in db_data:
        formatted_data.append(float(i[0].split("'")[0]))
        label_data.append(i[1].replace("T", " ").split(" ")[1])

    # Get graph as base64
    chart_data = _generate_graph(data=formatted_data, 
                                 labels=label_data, 
                                 graph_title=sensor)

    return chart_data






    

