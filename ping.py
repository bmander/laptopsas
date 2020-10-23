import pyaudio
import struct
import array

def square_wave( period, amp ):
    def ret(i):
        if i%period < period/2:
            return amp
        else:
            return -amp
    return ret

def tick( offset, amp ):
    def ret(i):
        if i<offset:
            return 0
        if i==offset:
            return amp
        if i==offset+1:
            return -amp
        return 0
    return ret

def encode_to_file( grid, datatype ):
    yield struct.pack( "ii", len(grid[0]), len(grid) )

    for row in grid:
        yield array.array( datatype, row ).tostring()

def encode_for_output( ary ):
    return array.array( "h", [int(a) for a in ary] ).tostring()

def decode_from_input( data ):
    ary = array.array("h")
    ary.fromstring( data )
    return ary

def main(fn, pinglen=0.25, nsamples=10):
    CHUNK = 1024
    RATE = 44100
    PLAYLEN = pinglen #seconds
    CHANNELS = 1
    FORMAT = pyaudio.paInt16

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    instream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    #func = square_wave(20000, 22000)
    func = tick(0, 22000)
    sample = [func(i) for i in range(int(PLAYLEN*RATE/CHUNK)*CHUNK)]


    rows = nsamples
    cols = int(PLAYLEN*RATE/CHUNK)*CHUNK
    fpout = open( fn, "w" )
    fpout.write( struct.pack( "II", rows, cols) )
    image = []
    for i in range(rows):
        row = []
        # play tick while listening
        for i in range(int(PLAYLEN*RATE/CHUNK)):
            stream.write( encode_for_output(sample[i*CHUNK:i*CHUNK+CHUNK]) )

            data = instream.read(CHUNK)
            ary = list(decode_from_input( data ))
            row.extend( ary )
        fpout.write( encode_for_output(row) )

    stream.stop_stream()
    stream.close()

    p.terminate()

import sys
if __name__=='__main__':
    if len(sys.argv)<2:
        print "usage: python ping.py filename [pinglen nsamples]"
        exit()
    fn = sys.argv[1]
    if len(sys.argv)>2:
        pinglen = float(sys.argv[2])
        nsamples = int(sys.argv[3])
        main( fn, pinglen, nsamples)
    else:
        main( fn )
