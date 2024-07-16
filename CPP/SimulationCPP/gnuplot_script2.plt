set term gif animate
set output 'pendulum.gif'
set xrange [0:5]
set yrange [0:5]
set size square
theta1_size = 201
theta3_size = 201
do for [i=1:theta1_size] {
    plot 'pendulum1.txt' every ::1::i with lines title 'Pendulum 1' lc rgb 'blue', \
         'pendulum3.txt' every ::1::i with lines title 'Pendulum 2' lc rgb 'green', \
}
