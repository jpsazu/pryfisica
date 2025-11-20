set title "Mapa de calor de current(x,y)"
set xlabel "X"
set ylabel "Y"

set pm3d map                  # activa pm3d en modo mapa 2D
set colorbox
set palette defined (0 "blue", 0.5 "yellow", 1 "red")


stats 'data.dat' using 1 nooutput
xmin = STATS_min
xmax = STATS_max

stats 'data.dat' using 2 nooutput
ymin = STATS_min
ymax = STATS_max



set xrange [xmin:xmax]
set yrange [ymin:ymax]
set size ratio -1             # mantiene proporción cuadrada

set cbrange [0:100]           # escala fija de temperatura

set terminal pngcairo size 800,600
set output 'grafico.png'

splot 'data.dat' using 1:2:3 with pm3d notitle



