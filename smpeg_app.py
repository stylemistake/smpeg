#!/usr/bin/python
import sys, time, PIL, getopt
from PIL import Image, ImageFilter, ImageChops
from smpeg_types import Container, Bitmap, counter

def convert( im, quality = 75, method = 2, **_kwargs ):
	ratio = 1. - float( quality ) * 0.01
	kwargs = {
		"threshold": 15 + 130 * ratio,
		"block_max": 8 + min( im.size ) * ratio / 16,
		"block_min": 3,
		"method": method
	}
	im.save("smpeg_test_1.png")

	sys.stdout.write("compacting... ")
	sys.stdout.flush()
	t_start = time.time()
	im = Container( im ).compact( **kwargs )
	t_end = time.time()
	print "\nCompacting time:", t_end - t_start

	t_start = time.time()
	im = im.render()
	t_end = time.time()
	print "Rendering time:", t_end - t_start

	print "params: ", kwargs
	print counter

	im.save("smpeg_test_2.png")
	return im

## Configuration
opts = {
	"quality": 75
}


## --------------------------------------------------------------------------
##   Getting commandline options
## --------------------------------------------------------------------------

def print_help():
	print "Usage: smpeg_app.py <options>"; tab = "   "
	print "Options:"
	print tab, "-i --input <file>: Input file (required)"
	print tab, "-q --quality <n>: Quality of compression, 0-100 (default: 75)"
	print tab, "-h --help: Display this help message"
	sys.exit(2)

try:
	getopt_opts, argv = getopt.getopt( sys.argv[1:], "+hq:m:i:", [
		"quality=", "method=", "input=", "help",
	])
except getopt.GetoptError:
	print "(error) invalid parameter(s)"; print_help()

for opt, arg in getopt_opts:
	if opt in ( "-q", "--quality" ): opts["quality"] = int( arg )
	if opt in ( "-m", "--method" ): opts["method"] = int( arg )
	if opt in ( "-i", "--input" ): opts["input"] = arg
	if opt in ( "-h", "--help" ): print_help()

if not "input" in opts:
	print "error: No input file is provided."
	sys.exit(2)

im = Image.open( opts["input"] )
# im = Image.open("lenna_64p.bmp")
# im = Image.open("doge.jpg")
# im.show()

# blur = PIL.ImageFilter.GaussianBlur( radius = 32 )
# blur = PIL.ImageFilter.MedianFilter( size = 9 )
# delta_image = PIL.ImageChops.difference( im, im.filter( blur ) )
# delta_image.show()

im = convert( im, **opts )
im.show()
# im = im.convert("L")
# im.show()
# convert( im, method = 1, threshold = 40, block_max = 128 ).show()
# convert( im, method = 2, threshold = 40, block_max = 128, block_min = 4 ).show()


# im.filter( blur ).show()
# im = im.resize( ( 2, 2 ), resample = PIL.Image.ANTIALIAS )
# im = im.resize( ( 64, 64 ), resample = PIL.Image.BICUBIC )

# im.show()