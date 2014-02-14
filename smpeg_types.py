#!/usr/bin/python
import sys, PIL

counter = {
	".": 0,
	"c": 0,
	"/": 0
}

def _log( msg ):
	counter[ msg ] += 1
	sys.stdout.write( msg )
	sys.stdout.flush()

class Color:
	def __init__( self, size, color ):
		self.size = size
		self.color = color

	def __repr__( self ):
		return repr( self.color )

	def render( self ):
		return PIL.Image.new( "RGB", list( self.size ), self.color )



class Gradient:
	def __init__( self, size, gradient ):
		self.size = size
		self.gradient = gradient

	def __repr__( self ):
		return repr( self.gradient.getdata() )

	def render( self ):
		return self.gradient.resize( self.size, resample = PIL.Image.BICUBIC )



class Bitmap:
	def __init__( self, image ):
		self.size = image.size
		self.image = image

	def __repr__( self ):
		return repr( self.to_list() )

	def get_area( self, coords ):
		size = ( coords[2] - coords[0], coords[3] - coords[1] )
		buf = PIL.Image.new( "RGB", list( size ) )
		buf.paste( self.image.crop( coords ), ( 0, 0 ) )
		return buf

	def get_list( self ):
		if not hasattr( self, "pixels" ):
			self.pixels = list( self.image.getdata() )
		return self.pixels

	def get_delta_map( self ):
		if not hasattr( self, "delta_map" ):
			blur = PIL.ImageFilter.GaussianBlur( radius = 64 )
			#blur = PIL.ImageFilter.MedianFilter( size = 9 )
			delta_image = PIL.ImageChops.difference( self.image, self.image.filter( blur ) )
			self.delta_map = list( delta_image.getdata() )
		return self.delta_map

	def get_average_color( self ):
		if not hasattr( self, "color_avg" ):
			pixel_list = self.get_list()
			r, g, b, c = ( 0, 0, 0, 0 )
			for pixel in pixel_list:
				r += pixel[0]
				g += pixel[1]
				b += pixel[2]
				c += 1
			self.color_avg = ( r/c, g/c, b/c )
		return self.color_avg

	def get_max_delta( self ):
		if not hasattr( self, "color_max_delta" ):
			# pixel_list = self.get_list()
			# average = sum( self.get_average_color() )
			# delta = 0
			# for pixel in pixel_list:
			# 	current = sum( pixel )
			# 	if abs( current - average ) > delta: delta = abs( current - average )
			# self.color_max_delta = delta

			pixel_list = self.get_delta_map()
			delta = 0
			for pixel in pixel_list:
				current = sum( pixel )
				if current > delta: delta = current
			self.color_max_delta = delta
		return self.color_max_delta

	def to_color( self ):
		return Color( self.size, self.get_average_color() )

	def to_gradient( self ):
		samp = self.image.resize( ( 2, 2 ), resample = PIL.Image.ANTIALIAS )
		return Gradient( self.size, samp )

	def render( self ):
		return self.image



class Container:
	def __init__( self, content ):
		if isinstance( content, PIL.Image.Image ):
			self.content = Bitmap( content )
		else:
			self.content = content
		self.size = content.size
		self.is_sliced = False

	def __repr__( self ):
		return repr( self.content )

	def slice( self ):
		w, h = self.size
		sw, sh = ( w/2, h/2 )
		if min( w, h ) < 2: return self
		bitmap = self.content
		self.is_sliced = True
		self.content = []
		self.mapping = [
			( 0, 0, sw, sh ),
			( sw, 0, w, sh ),
			( 0, sh, sw, h ),
			( sw, sh, w, h )
		]
		for coords in self.mapping:
			item = bitmap.get_area( coords )
			self.content.append( Container( item ) )
		return self

	def compact( self, method = 1, block_max = 8, block_min = 2, threshold = 80 ):
		kwargs = {
			"method": method, "block_max": block_max,
			"block_min": block_min, "threshold": threshold
		}
		bitmap = self.content

		# Slice until we get a right blocksize
		if max( *self.size ) > block_max:
			self.slice()
			for s in self.content: s.compact( **kwargs )

		else:
			delta = bitmap.get_max_delta()
			# If block looks good for compressing, do it
			if delta < threshold:
				_log("c")
				if method == 1: self.content = self.content.to_color()
				if method == 2: self.content = self.content.to_gradient()

			# Or slice it more for better detail
			elif min( *self.size ) > block_min:
				_log("/")
				self.slice()
				for s in self.content: s.compact( **kwargs )

			# Or leave the block entirely, it's good
			else: _log(".")

		return self

	def render( self ):
		if self.is_sliced:
			buf = PIL.Image.new( "RGB", list( self.size ), ( 0, 0, 0 ) )
			for ( item, box ) in zip( self.content, self.mapping ):
				buf.paste( item.render(), box[0:2] )
			return buf
		else:
			return self.content.render()
