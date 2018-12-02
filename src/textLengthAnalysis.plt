set terminal png size 800,500 enhanced 
set output 'textLengthAnalysis.png'

red = "#FF0000"; green = "#00FF00"; blue = "#0000FF"; black = "#000000"; white = "#999999"; purple = "#800080";

set style data histogram
set style histogram cluster gap 1
set style fill solid
set boxwidth 1

set xrange [0:15]
set yrange [0:25]

set xtics 5
set grid ytics

set xlabel "Words in Card Text"
set ylabel "Number of Cards"
set title "Card Text by Color"

plot "textLengthAnalysis.dat" using 2:xticlabels(1) title "White" linecolor rgb white, \
      '' using 3:xticlabels(1) title "Blue" linecolor rgb blue, \
      '' using 4:xticlabels(1) title "Black" linecolor rgb black, \
      '' using 5:xticlabels(1) title "Red" linecolor rgb red, \
      '' using 6:xticlabels(1) title "Green" linecolor rgb green, \
      '' using 7:xticlabels(1) title "Other" linecolor rgb purple
