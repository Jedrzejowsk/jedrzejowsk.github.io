set term gif animate
set output 'lorenz.gif'
set view 60, 30, 1, 1
set xrange [-30:30]
set yrange [-30:30]
set zrange [0:60]
set size square
do for [i=1:501] {
    splot 'lorenz1.txt' every ::1::i using 1:2:3 with lines title 'Lorenz 1', 'lorenz2.txt' every ::1::i using 1:2:3 with lines title 'Lorenz 2'
}
