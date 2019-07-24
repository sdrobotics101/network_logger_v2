set mouse

set datafile separator " "
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%M:%S"
set title 'apz'
set xlabel 'time'
set ylabel 'degrees'
set autoscale x
set yrange [-180:180]
set y2range [-110: 110]

set cbrange [0:5]
set palette model RGB
set palette defined (0 'black', 1 'red', 2 'green', 3 'blue', 4 'magenta', 5 'white')
unset colorbox

# 8 -> heading setpoint
# 9 -> control active
# 14 -> heading actual
# 15 -> angular active
# 16 -> killed

filename=ARG1
plot filename u 1:14:($15==0 ? 1 : 2) axes x1y1 title "actual" with lines palette, \
     filename u 1:8:($9==0 ? 1 : 3) axes x1y1 title "setpoint" with lines palette, \
     filename u 1:3:($9==0 ? 1 : 4) axes x1y2 title "lvx" with lines palette, \
     filename u 1:(105):($16==0 ? 0 : 5) axes x1y2 title "killed" with lines palette, \
