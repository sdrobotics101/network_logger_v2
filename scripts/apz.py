import sys
import time
import csv
from datetime import datetime

from bokeh.plotting import figure, output_file, show
from bokeh.models import BoxAnnotation

def main(args):
    timestamps = []
    setpoints = []
    actual = []
    killed = []
    if len(args) < 2:
        print("need input file")
        return
    with open(args[1], 'r') as f:
        reader = csv.DictReader(f, delimiter=' ')
        reader.fieldnames.pop(0)
        for row in reader:
            t = datetime.strptime(" ".join([row['date'], row['time']]), "%Y-%m-%d %H:%M:%S.%f")
            timestamps.append(t)
            setpoints.append(float(row['m_apz']))
            actual.append(float(row['s_apz']))
            killed.append(bool(float(row['killed'])))

    left_edges = []
    right_edges = []
    for i in range(1,len(killed)):
        if killed[i] and not killed[i-1]:
            left_edges.append(timestamps[i])
        if not killed[i] and killed[i-1]:
            right_edges.append(timestamps[i])

    print(left_edges)
    print(right_edges)

    if len(left_edges) != len(right_edges):
        right_edges.append(timestamps[len(timestamps)-1])

    p = figure(title="apz",
               x_axis_label="time",
               x_axis_type="datetime",
               y_axis_label="degrees",
               y_range=(-180,180),
               sizing_mode="stretch_both")
    p.line(timestamps, actual, color='green')
    p.line(timestamps, setpoints, color='blue')

    for i in range(len(left_edges)):
        box = BoxAnnotation(left=left_edges[i], right=right_edges[i], fill_color='red')
        p.add_layout(box)

    show(p)

if __name__ == "__main__":
    main(sys.argv)
