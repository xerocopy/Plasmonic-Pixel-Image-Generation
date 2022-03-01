########################################################################
##																	  ##
##		gdsCAD code for creating saturation corrected GDS image		  ##
##																	  ##
########################################################################

import os
import numpy
import colorsys
from gdsCAD import *
from numpy import *
from numpy import linalg as LA

########################################################################
##																	  ##
##		Layers for each colour have been set to 1 to reduce issues    ##
##      with Beamer		                                              ##
##																	  ##
########################################################################

# YELLOW ELEMENT AND PIXEL
yellow=core.Cell('YELLOW')

yelx = 0.075
yely = 0.05

yellow.add(shapes.Rectangle((.10,0),(yelx+0.1,yely),layer=1))


# MAGENTA ELEMENT AND PIXEL
magenta=core.Cell('MAGENTA')
magx = 0.090
magy = 0.05

magenta.add(shapes.Rectangle((0.085,0),(magx+0.085,magy),layer=2))


# CYAN ELEMENT AND PIXEL
cyan=core.Cell('CYAN')
cyax = 0.135
cyay = 0.05

cyan.add(shapes.Rectangle((0.075,0),(cyax+0.075,cyay),layer=3))


# BLACK ELEMENT AND PIXEL
black=core.Cell('BLACK')
bl1x = 0.085
bl1y = 0.05

bl2x = 0.055
bl2y = 0.05

# Is the location of the Black cells wrong???
black.add(shapes.Rectangle((0.085,0),(bl1x+0.085,bl1y),layer=4))
black.add(shapes.Rectangle((0.1,0.125),(bl2x+0.1,bl2y+0.125),layer=4))



SubU=core.Cell('SubU') 		# Constantly varying Cels
TotU=core.Cell('TotU')

# Import the image using Pillow, then convert to RGB and then to LAB to extract the s value
# for calculating the colour l
from PIL import Image
im = Image.open("george_daniel_de_monfreid_1889.jpg")
filename = 'm1.gds'
rgb_im = im.convert('RGB')
rgb_im = rgb_im.transpose(Image.FLIP_TOP_BOTTOM)

xsize, ysize = im.size
print xsize, ysize, 'rgb size'

from skimage import color
hsv = color.rgb2hsv(rgb_im)



for y in range(0, ysize):
	for x in range(0, xsize):
		print x, y, 'xy value'
		r, g, bl = rgb_im.getpixel((x, y))
		h, s, v = hsv[y,x]
# Hue value appears to be a 0-1 integer not 0-360deg
		print 'before h', h, 's', s, 'v', v
		s = s /0.5
		v = v /0.6
		print 'after h', h, 's', s, 'v', v
#		print r,'r',g,'g',bl,'b', '0 means black, 255 fuls colour/white'

# Extracting the RGB values just from the Hue to give the fully saturated colour which can
# then be converted into CMY - taken from http://www.cs.rit.edu/~ncs/color/t_convert.html
		h *= 6
		i = int(h)
		f = h - i
		p = 0
		q = (1-f)
		t = f

		if s == 0 and v == 1:
			red = 1
			gre = 1
			blu = 1
		elif v == 0:
			red = 0
			gre = 0
			blu = 0
		else:
			if i == 0:
				red = 1
				gre = t
				blu = 0
			elif i == 1:
				red = q
				gre = 1
				blu = 0
			elif i == 2:
				red = 0
				gre = 1
				blu = t
			elif i == 3:
				red = 0
				gre = q
				blu = 1
			elif i == 4:
				red = t
				gre = 0
				blu = 1
			elif i == 5:
				red = 1
				gre = 0
				blu = q


# Converting RGB to CMY without black, blu= blue
		c=1-red
		m=1-gre
		yl=1-blu
		print 'cyan',c,'magenta',m,'yellow',yl

# Calculating the Lightness of the colour, this will determine how white/black the pixel is
		Lmax = max(r,g,bl)
		Lmin = min(r,g,bl)
		L = (Lmax + Lmin)/float(510)
# 		print'Lmax', Lmax, 'Lmin', Lmin, 'L', float(L)


# Creating the CMY values in integer form summing to 10 to enable
# the creation of the 10x10um sub-pixes (SubU)
		if v != 0 and s != 0:
			cnorm = c - ((m+yl)/2)
			mnorm = m - ((c+yl)/2)
			ylnorm = yl - ((m+c)/2)

			Cr = c/(c+m+yl)
			Mr = m/(c+m+yl)
			Yr = yl/(c+m+yl)

			Crr = round(Cr,1)*10
			Mrr = round(Mr,1)*10
			Yrr = round(Yr,1)*10
	# 		print Crr, Mrr, Yrr, 'c m y'




	# If the totas amount of colour stripes after rounding is greater than 10, take 1 off the
	# lowest colour value as it has the least influence on the overall colour

			if Crr+Mrr+Yrr > 10:
				if Crr <= Mrr and Cr <= Yrr:
					Crr = Crr - 1
				elif Mrr <= Crr and Mrr <= Yrr:
					Mrr = Mrr - 1
				elif Yrr <= Crr and Yrr <= Mrr:
					Yrr = Yrr - 1

	# If the totas amount of colour stripes after rounding is less than 10, add 1 to the
	# highest colour value as it has the greatest influence on the overall colour

			if Crr+Mrr+Yrr < 10:
				if Crr >= Mrr and Cr >= Yrr:
					Crr = Crr + 1
				elif Mrr >= Crr and Mrr >= Yrr:
					Mrr = Mrr + 1
				elif Yrr >= Crr and Yrr >= Mrr:
					Yrr = Yrr + 1


		if v == 0:
			Value = 9
		elif v>=1:
			Value = 0
		else:
			Value = int((1-v)*10)

		# String used to build the pixel, black = 1, colour = 2, white = 3
		PixelString = [3,3,3,3,3,3,3,3,3]


		for a in range(0, Value):
			PixelString[a] = 1

		Leftover = 9 - Value


		###		saturation is between 0-1, it decides the number of white pixels. s=1 no white pixel


		if s >= 1:
			Sat = 9
		else:
			Sat = int(s*10)


		# Using the integer value of Saturation to determine how many colour sub pixels there are in the
		# leftover pixels from the black pixel calculation
		Colour = int((Sat/float(9))*Leftover)

		if  s*Leftover*float(1) - s*Leftover >= 0.5 :
			Colour += 1
		print 'L5.color adjustment:'
		print '   colour', Colour, 'value', Value, 'Leftover', Leftover
		# leftover should be improved !!!!

		if Value != 9:
			for a in range(Value, Colour + Value):
				PixelString[a] = 2

		print PixelString
		print Crr, Mrr, Yrr

# If pix values are based on colour values 1 = black, 2 = colour, 3 = white (blank), where
# a is the x coordinate and b the y coordinate in the 3x3 sub pixel in the array
#
# The second if loop in the code is used to make sure there isn't overlapping of C,M,Y in the
# first row of each pixel, which comes out in BEAMER, and only occationally in KLayout
#
		for a in range(0,3):
			for b in range(0,3):
				n = 3*(a-1) + b
				m = n - 1
				pix = PixelString[m]

				if pix == 1:
					array = core.CellArray(black, 40, 40, (0.25,0.25), origin=(x*30+10*(a-1),y*30+10*(b-1)))
					SubU.add(array)
					print 'noblack'
				elif pix == 2:
					if Crr >= 1 and Mrr == 0 and Yrr == 0:
						array = core.CellArray(cyan, Crr*3.3, 33, (0.30,0.30), origin=(x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
					elif Mrr >= 1 and Yrr == 0 and Crr == 0:
						array = core.CellArray(magenta, Mrr*3.3, 33, (0.30,0.30), origin=(x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
					elif Yrr >= 1 and Mrr == 0 and Crr == 0:
						array = core.CellArray(yellow, Yrr*3.3, 62.5, (0.30,0.16), origin=(x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
					elif Crr >= 1 and Mrr >= 1 and Yrr == 0:
						array = core.CellArray(cyan, Crr*3.3, 33, (0.30,0.30), origin=(x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
						array = core.CellArray(magenta, Mrr*3.3, 33, (0.30,0.30), origin=(Crr+x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
					elif Crr >= 1 and Yrr >= 1 and Mrr == 0:
						array = core.CellArray(cyan, Crr*3.3, 33, (0.30,0.30), origin=(x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
						array = core.CellArray(yellow, Yrr*3.3, 62.5, (0.30,0.16), origin=(Crr+x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
					elif Yrr >= 1 and Mrr >= 0 and Crr == 0:
						array = core.CellArray(magenta, Mrr*3.3, 33, (0.30,0.30), origin=(x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
						array = core.CellArray(yellow, Yrr*3.3, 62.5, (0.30,0.16), origin=(Mrr+x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
					elif Yrr >= 1 and Mrr >= 1 and Crr >= 1:
						array = core.CellArray(cyan, Crr*3.3, 33, (0.30,0.30), origin=(x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
						array = core.CellArray(magenta, Mrr*3.3, 33, (0.30,0.30), origin=(Crr+x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
						array = core.CellArray(yellow, Yrr*3.3, 62.5, (0.30,0.16), origin=(Crr+Mrr+x*30+10*(a-1),y*30+10*(b-1)))
						SubU.add(array)
					print 'colour'
				else:
					print 'white'


print 'done'


# Create a layout and add the cell
layout = core.Layout('LIBRARY')
layout.add(SubU)

# Save the layout and then display it on screen
layout.save('test.gds')
# layout.show()
