#### This is version 2.0 to improve saturation correction mechanism ####
#### Fabricated sample 20191024 #4 v4 ####


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

# global parameters
P = 0.23

Dr = 0.18
Lr = 0.18

Dg = 0.14
Lg = 0.18

Db = 0.16
Lb = 0.18

# sub pixel size(width in x direction) shrink down from 10um to 9.2um

# RED ELEMENT AND PIXEL D180 L180 P230
redd=core.Cell('RED')
redd.add(shapes.Rectangle((0.02,0),(0.04,0.18),layer=1))
redd.add(shapes.Rectangle((0.04,0),(0.06,0.18),layer=2))
redd.add(shapes.Rectangle((0.06,0),(0.08,0.18),layer=3))
redd.add(shapes.Rectangle((0.08,0),(0.10,0.18),layer=4))
redd.add(shapes.Rectangle((0.10,0),(0.12,0.18),layer=5))
redd.add(shapes.Rectangle((0.12,0),(0.14,0.18),layer=6))
redd.add(shapes.Rectangle((0.14,0),(0.16,0.18),layer=7))
redd.add(shapes.Rectangle((0.16,0),(0.18,0.18),layer=8))
redd.add(shapes.Rectangle((0.18,0),(0.20,0.18),layer=9))

# GREEN ELEMENT AND PIXEL D140 L180 P230
green=core.Cell('GREEN')
green.add(shapes.Rectangle((0.02,0),(0.04,0.14),layer=1))
green.add(shapes.Rectangle((0.04,0),(0.06,0.14),layer=2))
green.add(shapes.Rectangle((0.06,0),(0.08,0.14),layer=3))
green.add(shapes.Rectangle((0.08,0),(0.10,0.14),layer=4))
green.add(shapes.Rectangle((0.10,0),(0.12,0.14),layer=5))
green.add(shapes.Rectangle((0.12,0),(0.14,0.14),layer=6))
green.add(shapes.Rectangle((0.14,0),(0.16,0.14),layer=7))
green.add(shapes.Rectangle((0.16,0),(0.18,0.14),layer=8))
green.add(shapes.Rectangle((0.18,0),(0.20,0.14),layer=9))

# BLUE ELEMENT AND PIXEL D160 L180 P230
blue=core.Cell('BLUE')
blue.add(shapes.Rectangle((0.02,0),(0.04,0.16),layer=1))
blue.add(shapes.Rectangle((0.04,0),(0.06,0.16),layer=2))
blue.add(shapes.Rectangle((0.06,0),(0.08,0.16),layer=3))
blue.add(shapes.Rectangle((0.08,0),(0.10,0.16),layer=4))
blue.add(shapes.Rectangle((0.10,0),(0.12,0.16),layer=5))
blue.add(shapes.Rectangle((0.12,0),(0.14,0.16),layer=6))
blue.add(shapes.Rectangle((0.14,0),(0.16,0.16),layer=7))
blue.add(shapes.Rectangle((0.16,0),(0.18,0.16),layer=8))
blue.add(shapes.Rectangle((0.18,0),(0.20,0.16),layer=9))


# BLACK ELEMENT AND PIXEL
black=core.Cell('BLACK')
black.add(shapes.Rectangle((0.02,0),(0.04,0.2),layer=1))
black.add(shapes.Rectangle((0.04,0),(0.06,0.2),layer=2))
black.add(shapes.Rectangle((0.06,0),(0.08,0.2),layer=3))
black.add(shapes.Rectangle((0.08,0),(0.10,0.2),layer=4))
black.add(shapes.Rectangle((0.10,0),(0.12,0.2),layer=5))
black.add(shapes.Rectangle((0.12,0),(0.14,0.2),layer=6))
black.add(shapes.Rectangle((0.14,0),(0.16,0.2),layer=7))
black.add(shapes.Rectangle((0.16,0),(0.18,0.2),layer=8))
black.add(shapes.Rectangle((0.18,0),(0.22,0.2),layer=9))

'''
bl1x = 0.085
bl1y = 0.05
bl2x = 0.055
bl2y = 0.05
# Is the location of the Black cells wrong???
black.add(shapes.Rectangle((0.085,0),(bl1x+0.085,bl1y),layer=1))
black.add(shapes.Rectangle((0.1,0.125),(bl2x+0.1,bl2y+0.125),layer=1))
'''

SubU=core.Cell('SubU') 		# Constantly varying Cels
TotU=core.Cell('TotU')

# size = 230 nm x 400 = 9.2 um
# generate the color gamut underneath the image for referencing
array = core.CellArray(redd, 4000, 4000, (P,P), origin=(0,-1500))
SubU.add(array)
array = core.CellArray(green, 4000, 4000, (P,P), origin=(2000,-1500))
SubU.add(array)
array = core.CellArray(blue, 4000, 4000, (P,P), origin=(2000*2,-1500))
SubU.add(array)
array = core.CellArray(black, 4000, 4000, (P,P), origin=(2000*3,-1500))
SubU.add(array)


# Import the image using Pillow, then convert to RGB and then to LAB to extract the s value
# for calculating the colour l
from PIL import Image
#im = Image.open("colors.jpg")
im = Image.open("Van_Gogh.jpg")
filename = 'm1.gds'
rgb_im = im.convert('RGB')
rgb_im = rgb_im.transpose(Image.FLIP_TOP_BOTTOM)

xsize, ysize = im.size
print 'L1.image size:', 'xsize', xsize,'ysize', ysize, 'rgb size'

from skimage import color
hsv = color.rgb2hsv(rgb_im)



for y in range(0, ysize):
	for x in range(0, xsize):
		print 'L2.pixel location:','x', x, 'y', y
		r, gr, bl = rgb_im.getpixel((x, y))
		h, s, v = hsv[y,x]
# Hue value appears to be a 0-1 integer not 0-360deg
		print 'L3.color intepretation:','h', h, 's', s, 'v', v, 'r', r,'gr', gr, 'bl', bl
		s = s /0.6
		v = v /0.6
		print '   color enhancement','h', h, 's', s, 'v', v, 'r', r,'gr', gr, 'bl', bl
		print '   !note: 0 means black, 255 fuls colour/white!'

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
#
# # Modified by Jingchao, so the RGB value are kept in RGB, without converting to CMY
# # Converting RGB to CMY without black, blu= blue
# 		c=1-red
# 		m=1-gre
# 		yl=1-blu
 		print '  ','red',red,'green',gre,'blue',blu

# Calculating the Lightness of the colour, this will determine how white/black the pixel is
		Lmax = max(r,gr,bl)
		Lmin = min(r,gr,bl)
		L = (Lmax + Lmin)/float(510)
#		print'Lmax', Lmax, 'Lmin', Lmin, 'L', float(L)


# # Creating the CMY values in integer form summing to 10 to enable
# # the creation of the 10x10um sub-pixes (SubU)
# 		if v != 0 and s != 0:
# 			cnorm = c - ((m+yl)/2)
# 			mnorm = m - ((c+yl)/2)
# 			ylnorm = yl - ((m+c)/2)
#
# 			Cr = c/(c+m+yl)
# 			Mr = m/(c+m+yl)
# 			Yr = yl/(c+m+yl)
#
# 			Crr = round(Cr,1)*10
# 			Mrr = round(Mr,1)*10
# 			Yrr = round(Yr,1)*10
# 	# 		print Crr, Mrr, Yrr, 'c m y'


		if v != 0 and s != 0:
			# rnorm = r - ((g+bl)/2)
			# gnorm = g - ((r+bl)/2)
			# blnorm = bl - ((r+g)/2)

			Rr = red/(red+gre+blu)
			Gr = gre/(red+gre+blu)
			Br = blu/(red+gre+blu)

			Rrr = round(Rr,1)*10
			Grr = round(Gr,1)*10
			Brr = round(Br,1)*10

#			print 'Rr', Rr, 'Gr', Gr, 'Br', Br
#			print 'Rrr', Rrr, 'Grr', Grr, 'Brr', Brr
	# If the totas amount of colour stripes after rounding is greater than 10, take 1 off the
	# lowest colour value as it has the least influence on the overall colour

			if Rrr+Grr+Brr > 10:
				if Rrr <= Grr and Rrr <= Brr:
					Rrr = Rrr - 1
				elif Grr <= Rrr and Grr <= Brr:
					Grr = Grr - 1
				elif Brr <= Rrr and Brr <= Grr:
					Brr = Brr - 1

	# If the totas amount of colour stripes after rounding is less than 10, add 1 to the
	# highest colour value as it has the greatest influence on the overall colour

			if Rrr+Grr+Brr < 10:
				if Rrr >= Grr and Rrr >= Brr:
					Rrr = Rrr + 1
				elif Grr >= Rrr and Grr >= Brr:
					Grr = Grr + 1
				elif Brr >= Rrr and Brr >= Grr:
					Brr = Brr + 1

			print 'L4.RGB analysis:'
			print '   RGB wight in %:', 'Rr', Rr, 'Gr', Gr, 'Br', Br
			print '   Rounded RGB %','Rrr', Rrr, 'Grr', Grr, 'Brr', Brr


###		value is between 0-1, it decides the number of black pixels, v = 1 no black pixel

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

#		print PixelString
#		print 'Rrr', Rrr, 'Grr', Grr, 'Brr', Brr

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
					array = core.CellArray(black, 40, 40, (P,P), origin=(x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
					SubU.add(array)
					print 'black'
				elif pix == 2:
					if Rrr >= 1 and Grr == 0 and Brr == 0:
						array = core.CellArray(redd, Rrr*4, 9.2/P+1, (P,P), origin=(x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
					elif Grr >= 1 and Brr == 0 and Rrr == 0:
						array = core.CellArray(green, Grr*4, 9.2/P+1, (P,P), origin=(x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
					elif Brr >= 1 and Grr == 0 and Rrr == 0:
						array = core.CellArray(blue, Brr*4, 9.2/P+1, (P,P), origin=(x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)

					elif Rrr >= 1 and Grr >= 1 and Brr == 0:
						array = core.CellArray(redd, Rrr*4, 9.2/P+1, (P,P), origin=(x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
						array = core.CellArray(green, Grr*4, 9.2/P+1, (P,P), origin=(Rrr*P*4+x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
					elif Rrr >= 1 and Brr >= 1 and Grr == 0:
						array = core.CellArray(redd, Rrr*4, 9.2/P+1, (P,P), origin=(x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
						array = core.CellArray(blue, Brr*4, 9.2/P+1, (P,P), origin=(Brr*P*4+x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
					elif Brr >= 1 and Grr >= 1 and Rrr == 0:
						array = core.CellArray(green, Grr*4, 9.2/P+1, (P,P), origin=(x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
						array = core.CellArray(blue, Brr*4, 9.2/P+1, (P,P), origin=(Grr*P*4+x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)

					elif Brr >= 1 and Grr >= 1 and Rrr >= 1:
						array = core.CellArray(redd, Rrr*4, 9.2/P+1, (P,P), origin=(x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
						array = core.CellArray(green, Grr*4, 9.2/P+1, (P,P), origin=(Rrr*P*4+x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
						array = core.CellArray(blue, Brr*4, 9.2/P+1, (P,P), origin=((Rrr+Grr)*P*4+x*27.6+9.2*(a-1),y*27.6+9.2*(b-1)))
						SubU.add(array)
					print 'colour'
				else:
					print 'white'


print 'done'


# Create a layout and add the cell
layout = core.Layout('LIBRARY')
layout.add(SubU)

# Save the layout and then display it on screen
#layout.save('20191018_v3_test.gds')
layout.save('test.gds')
# layout.show()
