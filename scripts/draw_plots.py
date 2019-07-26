#!/usr/bin/env python3

import sys
import time
import csv
from datetime import datetime

from bokeh.plotting import figure, output_file, show
from bokeh.models import BoxAnnotation, LinearAxis, Range1d, HoverTool
from bokeh.palettes import Category10
import itertools

def main(args):
    timestamps = []
    x_setpoint = []
    y_setpoint = []
    z_setpoint = []
    d_setpoint = []
    x_actual = []
    y_actual = []
    z_actual = []
    d_actual = []
    lvx = []
    m0 = []
    m1 = []
    m2 = []
    m3 = []
    m4 = []
    m5 = []
    killed = []
    if len(args) < 2:
        print("need input file")
        return
    with open(args[1], 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = datetime.strptime(" ".join([row['date'], row['time']]), "%Y-%m-%d %H:%M:%S.%f")
            timestamps.append(t)
            x_setpoint.append(float(row['m_apx']))
            y_setpoint.append(float(row['m_apy']))
            z_setpoint.append(float(row['m_apz']))
            d_setpoint.append(float(row['m_lpz']))
            x_actual.append(float(row['s_apx']))
            y_actual.append(float(row['s_apy']))
            z_actual.append(float(row['s_apz']))
            d_actual.append(float(row['s_lpz']))
            m0.append(float(row['motor0']))
            m1.append(float(row['motor1']))
            m2.append(float(row['motor2']))
            m3.append(float(row['motor3']))
            m4.append(float(row['motor4']))
            m5.append(float(row['motor5']))
            lvx.append(float(row['m_lvx']))
            killed.append(bool(float(row['killed'])))

    rising_edges = []
    falling_edges = []
    if killed[0]:
        rising_edges.append(timestamps[0])
    for i in range(1,len(killed)):
        if killed[i] and not killed[i-1]:
            rising_edges.append(timestamps[i])
        if not killed[i] and killed[i-1]:
            falling_edges.append(timestamps[i])
    if len(rising_edges) != len(falling_edges):
        falling_edges.append(timestamps[-1])

    # TODO replace title with name of directory
    p = figure(title=str(timestamps[0]),
               x_axis_label="time (s)",
               x_axis_type="datetime",
               y_axis_label="orientation (degrees)",
               y_range=(-180,180),
               sizing_mode="stretch_both")
    p.extra_y_ranges = {"lvx": Range1d(start=-150,end=150),
                        "depth": Range1d(start=4, end=-1),
                        "motors": Range1d(start=-400, end=400)}
    p.add_layout(LinearAxis(y_range_name="lvx", axis_label="velocity"), 'left')
    p.add_layout(LinearAxis(y_range_name="depth", axis_label="depth (meters)"), 'left')
    p.add_layout(LinearAxis(y_range_name="motors", axis_label="motors"), 'left')

    colors = itertools.cycle(Category10[10])
    p.line(timestamps, x_actual, color=next(colors), legend="x_actual")
    p.line(timestamps, y_actual, color=next(colors), legend="y_actual")
    p.line(timestamps, z_actual, color=next(colors), legend="z_actual")
    p.line(timestamps, d_actual, color=next(colors), legend="d_actual", y_range_name="depth")
    p.line(timestamps, x_setpoint, color=next(colors), legend="x_setpoint")
    p.line(timestamps, y_setpoint, color=next(colors), legend="y_setpoint")
    p.line(timestamps, z_setpoint, color=next(colors), legend="z_setpoint")
    p.line(timestamps, d_setpoint, color=next(colors), legend="d_setpoint", y_range_name="depth")
    p.line(timestamps, lvx, color=next(colors), legend="lvx", y_range_name="lvx")
    p.line(timestamps, m0, color=next(colors), legend="m0", y_range_name="motors")
    p.line(timestamps, m1, color=next(colors), legend="m1", y_range_name="motors")
    p.line(timestamps, m2, color=next(colors), legend="m2", y_range_name="motors")
    p.line(timestamps, m3, color=next(colors), legend="m3", y_range_name="motors")
    p.line(timestamps, m4, color=next(colors), legend="m4", y_range_name="motors")
    p.line(timestamps, m4, color=next(colors), legend="m4", y_range_name="motors")

    for i in range(len(rising_edges)):
        box = BoxAnnotation(left=rising_edges[i], right=falling_edges[i], fill_color='red')
        p.add_layout(box)

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"

    p.add_tools(HoverTool())
    # Box Zoom tool is the third so use index 2
    p.toolbar.active_drag = p.tools[2]

    show(p)

if __name__ == "__main__":
    # TODO parse args and add a nice selection menu
    main(sys.argv)
