import struct
import array
from matplotlib import pyplot as plt
import numpy as np

def massage( rows ):
	image = []
	for row in rows:
		# high pass filter
	    spec = np.fft.rfft( row )
	    spec[0:len(spec)/2] = 0
	    row = np.fft.irfft( spec )

	    # grab the outgoing tick
	    peak = np.argmax( row )
	    tick = row[peak-5:peak+20]

	    # cross-correlate to get the echo
	    echo = np.correlate( row, tick, "valid" )

	    # find the primary from the echo and cut the sample down
	    peak = np.argmax( echo )
	    echo = echo[peak:peak+3500]

	    imrow = np.log(np.abs(echo))
	    #print min(imrow), max(imrow)

	    image.append( imrow )
	return image

def display(rows):
	plt.imshow( massage(rows), aspect="auto" )
	plt.show()

def read_pingfile( fn ):
	# open file
	fp = open( fn )

	# get number of pings, number of samples per ping
	nrows, ncols = struct.unpack_from( "II", fp.read(8) )

	# read pings
	rows = []
	for i in range(nrows):
		row = array.array("h")
		row.fromfile( fp, ncols )

		yield list(row) 

def main(fn):
	rows = read_pingfile(fn)
	display( rows )

import sys
if __name__=='__main__':
	fn = sys.argv[1]
	main( fn )
