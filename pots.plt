set autoscale

plot	'pots.txt' using 1:2 with lines title 'lin', \
		'pots.txt' using 1:3 with lines title '50K', \
		'pots.txt' using 1:4 with lines title '100K', \
		'pots.txt' using 1:5 with lines title '150K', \
		'pots.txt' using 1:6 with lines title '200K', \
		'pots.txt' using 1:7 with lines title '250K'
