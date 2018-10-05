set terminal png size 800,500 enhanced 
set output 'colorAnalysis.png'

red = "#FF0000"; green = "#00FF00"; blue = "#0000FF"; black = "#000000"; white = "#999999"; purple = "#800080";

set style data histogram
set style histogram cluster gap 1
set style fill solid
set boxwidth 1

set xrange [0:10]
set yrange [0:25]

set xtics 1
set grid ytics

set xlabel "Mana Cost"
set ylabel "Number of Cards"
set title "Cards per Color"

plot "colorAnalysis.dat" using 1 title "White" linecolor rgb white, \
      '' using 2 title "Blue" linecolor rgb blue, \
      '' using 3 title "Black" linecolor rgb black, \
      '' using 4 title "Red" linecolor rgb red, \
      '' using 5 title "Green" linecolor rgb green, \
      '' using 6 title "Other" linecolor rgb purple
