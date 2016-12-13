import time

import sqlite3
import pygal
from pygal.style import CleanStyle

import core.config as config

# Database is in a fixed location relative to installation path
DB_CONN = sqlite3.connect(config.local_path + '/db/pi_control.db')
DB_CUR = DB_CONN.cursor()


def _generate_graph(data, labels, graph_title=""):

    # Use subdivision of data length for major points
    label_count = int(len(data)/12)

    # Format graph
    line_chart = pygal.Line(width=500, height=400,
                            style=CleanStyle,
                            show_legend=False,
                            x_label_rotation=90,
                            x_labels_major_count=label_count,
                            show_minor_y_labels=True,
                            show_minor_x_labels=False,
                            show_only_major_dots=True,
                            dots_size=3,
                            title=graph_title + " (24hrs)",
                            font_family="Arial, Helvetica, sans-serif",
			    colors=("#E853A0"))

    line_chart.add('', data)
    line_chart.x_labels = labels

    return line_chart.render_data_uri()
    

def render_sensor_data(sensor, db_cursor=DB_CUR, table="sensor_data", date_column="record_date"):
    # Get SQL data
    db_data = db_cursor.execute("SELECT " + sensor + "," + date_column + \
                                " FROM " + table + \
                                " WHERE strftime('%Y-%m-%dT%H:%M:%S', " + date_column + ") >= strftime('%Y-%m-%dT%H:%M:%S', 'now', '-1 day')" + \
                                " ORDER BY strftime('%Y-%m-%dT%H:%M:%S'," + date_column + ")")

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






    

