#!/usr/bin/env python

'''
take a list of addresses and geocode them
Requires pygeocoder ('pip install pygeocoder' on the command line)
'''
import datetime
import sys

import isocronut

def usage():
	print ''
	print 'Usage: '+ sys.argv[0] + '[origin] [duration] [angles] [tolerance]'
	print '    origin : Either street address or lat,lon. e.g.: '
	print '             "350 5th Avenue, New York, NY 10118" or '
	print '             "40.74844,-73.985664"                   '
	print '   duration: drive time in minutes'
	print '     angles: how many bearings to calculate this contour for (think of this like resolution)'
	print '  tolerance: how many minutes within the exact answer for the contour is good enough'
	print ''
	print 'Example:'
	print  sys.argv[0] + ' "40.74844,-73.985664" 20 12 0.1'
	print ''

def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	if len(argv) != 5:
		usage()
		return 1
	
	origin = argv[1]
	duration = int(argv[2])
	number_of_angles = int(argv[3])
	tolerance = float(argv[4])

	print '%s:Generating...'%(datetime.datetime.now())
	isochrone = isocronut.generate_isochrone_map(origin, duration, number_of_angles=number_of_angles, tolerance=tolerance)
	print '%s:Done. Check isochrone.html in this directory.'%(datetime.datetime.now())

if __name__ == "__main__":
    sys.exit(main())
