set terminal x11
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
set y2range [-1:1]

set cbrange [0:3]
set palette defined (0 'black', 1 'red', 2 'green', 3 'blue')
unset colorbox

filename=ARG1
plot filename u 1:14:($15==0?0:1) axes x1y1 title "actual" with lines palette, \
     filename u 1:8:($9==0?0:2)  axes x1y1 title "setpoint" with lines palette, \
     filename u 1:16:($17==0?0:3) axes x1y2 title "killed" with lines palette
