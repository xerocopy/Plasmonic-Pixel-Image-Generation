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

# Black ELEMENT AND PIXEL D190 L180 P230
black=core.Cell('black')

black.add(shapes.Rectangle((0.02,0),(0.04,0.19),layer=1))
black.add(shapes.Rectangle((0.04,0),(0.06,0.19),layer=2))
black.add(shapes.Rectangle((0.06,0),(0.08,0.19),layer=3))
black.add(shapes.Rectangle((0.08,0),(0.10,0.19),layer=4))
black.add(shapes.Rectangle((0.10,0),(0.12,0.19),layer=5))
black.add(shapes.Rectangle((0.12,0),(0.14,0.19),layer=6))
black.add(shapes.Rectangle((0.14,0),(0.16,0.19),layer=7))
black.add(shapes.Rectangle((0.16,0),(0.18,0.19),layer=8))
black.add(shapes.Rectangle((0.18,0),(0.20,0.19),layer=9))


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


# BLUE-GREEN ELEMENT AND PIXEL D150 L180 P230
blueg=core.Cell('BLUEG')
blueg.add(shapes.Rectangle((0.02,0),(0.04,0.15),layer=1))
blueg.add(shapes.Rectangle((0.04,0),(0.06,0.15),layer=2))
blueg.add(shapes.Rectangle((0.06,0),(0.08,0.15),layer=3))
blueg.add(shapes.Rectangle((0.08,0),(0.10,0.15),layer=4))
blueg.add(shapes.Rectangle((0.10,0),(0.12,0.15),layer=5))
blueg.add(shapes.Rectangle((0.12,0),(0.14,0.15),layer=6))
blueg.add(shapes.Rectangle((0.14,0),(0.16,0.15),layer=7))
blueg.add(shapes.Rectangle((0.16,0),(0.18,0.15),layer=8))
blueg.add(shapes.Rectangle((0.18,0),(0.20,0.15),layer=9))

# GREEN ELEMENT AND PIXEL D130 L180 P230
green2=core.Cell('GREEN2')
green2.add(shapes.Rectangle((0.02,0),(0.04,0.13),layer=1))
green2.add(shapes.Rectangle((0.04,0),(0.06,0.13),layer=2))
green2.add(shapes.Rectangle((0.06,0),(0.08,0.13),layer=3))
green2.add(shapes.Rectangle((0.08,0),(0.10,0.13),layer=4))
green2.add(shapes.Rectangle((0.10,0),(0.12,0.13),layer=5))
green2.add(shapes.Rectangle((0.12,0),(0.14,0.13),layer=6))
green2.add(shapes.Rectangle((0.14,0),(0.16,0.13),layer=7))
green2.add(shapes.Rectangle((0.16,0),(0.18,0.13),layer=8))
green2.add(shapes.Rectangle((0.18,0),(0.20,0.13),layer=9))



SubU=core.Cell('SubU') 		# Constantly varying Cels
TotU=core.Cell('TotU')

# size = 230 nm x 400 = 9.2 um
# generate the color gamut underneath the image for referencing
#array = core.CellArray(redd, 4000, 4000, (P,P), origin=(0,-1500))
#SubU.add(array)

#array = core.CellArray(green, 21739, 21739, (P,P), origin=(2000,-1500))
#SubU.add(array)
#array = core.CellArray(green, 4347, 4347, (P,P), origin=(2000,-1500))
#SubU.add(array)

#array = core.CellArray(blue, 21739, 21739, (P,P), origin=(2000*2,-1500))
#SubU.add(array)

array = core.CellArray(black, 4347, 4347, (P,P), origin=(2000*2,-1500))
SubU.add(array)


#array = core.CellArray(black, 4000, 4000, (P,P), origin=(2000*3,-1500))
#SubU.add(array)

print 'done'


# Create a layout and add the cell
layout = core.Layout('LIBRARY')
layout.add(SubU)

# Save the layout and then display it on screen
layout.save('20191119_K190L180_POC1mm.gds')
# layout.show()
