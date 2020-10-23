from view import read_pingfile, massage

def dist( x0,y0,z0, x1,y1,z1 ):
	return ((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)**0.5

def generate_hypothesis( length, samples, h, x0, y0, pulsewidth=0.0004, samplesize=3500, rate=44100, soundspeed=340.29, amp=1 ):
	# radar array moves along the y axis

	spacing = length / float(samples)

	for i in range(samples):
		sample = [0]*samplesize

		y = spacing*i
		x = 0
		z = 0

		dd = dist(x,y,z,x0,y0,h)
		delay = (dd / soundspeed)*2

		if delay > samplesize/float(rate):
			yield sample
			continue

		pulsestart = int(delay*rate)
		pulseend = min(samplesize, int(pulsestart+pulsewidth*rate))
		for i in range(pulsestart, pulseend):
			sample[i] = amp
		yield sample

from matplotlib import pyplot as plt
import numpy as np

def main(fn):
    ss = massage( read_pingfile( fn ) )

    plt.imshow( ss, aspect="auto" )
    plt.show()

    rows = []
    for y in np.arange(0,10,0.1):
            row = []
            for x in np.arange(0.0,8.0,0.1):
                    print x,y,
                    ss_xy = np.array(list(generate_hypothesis( 10.4, 400, 2.0, x, y )))

                    refl_mat = ss_xy*ss
                    refl = np.sum(refl_mat)

                    row.append( refl )
            rows.append( row )

            # # save images as we go along
            # plt.imshow( rows, aspect="auto" )
            # plt.savefig( "/Users/brandon/Documents/%s-plot.png"%(y,))

    plt.imshow( rows, aspect="auto")
    plt.show()

if __name__=='__main__':

    pingfile="data/exterior.sonar"

    main(pingfile)
