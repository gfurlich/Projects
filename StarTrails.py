#!/usr/bin/env python
'''
File : StarTrails.py
Author : Greg Furlich
Date Created : 11/24/2017

Purpose : Simulate Star Trails for a random array of nstars around a randomly placed rotational axis for a length of nangle.

Execution : StarTrails.py <nstars> <nangle>

Example Execution : StarTrails.py 20 30

'''

#--- Start of Script ---#

#--- Importing Python Modules ---#

import sys
import random
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time
import math
from colorsys import hsv_to_rgb

#--- Initial Parameters ---#

# date generated :
#date = time.strftime('v%Y%m%d_%H%M%S')	# with sec percision
date = time.strftime('v%Y%m%d') # with day percision

pi = 3.14159265359

# Defining Rectangular window for plot :
# 16:9 aspect ratio

w = 1600	# width
h = 900		# height

# Number of Stars :
n_stars = int(sys.argv[1])

# Angle of Rotation (in Radians):
n_angle = float(sys.argv[2]) * pi / 180

# Steps of Rotation :
n_rotations = 10000

# Angle Steps :
delta_angle = n_angle / n_rotations 

#--- Star Initial Positions ---#
#print 'Star Initial Positions :'

# defining nstar and preallocate array :
star_x = [[] for _ in xrange(n_stars)]	# stars x position nested list
star_y = [[] for _ in xrange(n_stars)]	# stars y position nested list

star_initial_x =  []	# stars x position list
star_initial_y =  []	# stars y position list

# Randomly Defining Stars Position :
for i in range(0,n_stars):
	star_initial_x.append(random.uniform(-w,w))
	star_initial_y.append(random.uniform(-h,h))

	#print 'Star '+str(i+1)+' (star_x, star_y) = \t('+str(star_initial_x[i])+','+str(star_initial_y[i])+')'
'''
# Copying list to nested list :
star_x.append( star_initial_x )
star_y.append( star_initial_y )
'''
# Defining Random Rotational Axis :
rotational_axis_x = random.uniform(0,w)
rotational_axis_y = random.uniform(0,h)

#--- Plot Initial Star and Rotational Positions ---#
plt.figure(1)		# First Plot

plt.plot(star_initial_x, star_initial_y, '*')	# Star Plot
plt.plot(rotational_axis_x, rotational_axis_y, 'o')			# Rotation Point Plot
plt.xlim([0,w])		# X Range
plt.ylim([0,h])		# Y Range
plt.savefig("Stars_Initial_"+date+".png")	# Save Plot

#--- Rotate Stars ---#

# preallocate star array
star_r = [] 			# stars r list
star_initial_angle_d = [] 	# stars initial angle from rotational axis in degrees
star_initial_angle = []		# stars initial angle from rotational axis

# Calculate the radial distance between each star and axis :

for i in range(0,n_stars):
	delta_x = star_initial_x[i] - rotational_axis_x
	delta_y = star_initial_y[i] - rotational_axis_y
	star_r.append( math.sqrt(math.pow(delta_x,2) + math.pow(delta_y,2) ) )
	star_initial_angle_d.append( math.atan2( delta_y, delta_x ) * 180 / pi )
	star_initial_angle.append( math.atan2( delta_y, delta_x ) )
	#print 'Star '+str(i+1)+' (Radial Dist, Angle) = \t('+str(star_r[i])+', '+str(star_initial_angle[i])+')'
	#print 'Star '+str(i+1)+' (delta_x, delta_y) = \t('+str(delta_x)+', '+str(delta_y)+')'

# Calculate the movement of the star rotation :
#print ''
#print 'Calculated Star Movement :'

#star_trail = plt.figure(2, frameon=False)	# Second Plot
star_trail = plt.figure(2, frameon=False)

plt.xlim([0,w])		# X Range
plt.ylim([0,h])		# Y Range

# List for Star Size, Alpha, and Color:
star_size = []
star_color = []
star_alpha = []

# Background colors for the sky:
#bg = '#152033'
bg = '#000814'

for j in range(0,n_stars):

	print 'Rendering Trail for Star {0}\r'.format(j+1),

	# Star Random Size and Alpha :

	# Uniform Distribution Sampling :
	#star_size.append(float(random.uniform(.001,1)))
	#star_alpha.append(float(random.uniform(.5,1)))

	# Gaussian Distribution Sampling :
	#star_size.append(float(random.gauss(.01,.1) ) )
	star_alpha.append(float(random.gauss(.9,.01) ) )

	# Beta Distribution Sampling (skewed distribution):
	star_size.append( random.betavariate(2,4) )	

	# Star Random Color Variation from White :
	# White in HSV (0,0,1)
	h = random.uniform(0, 1)
	s = random.uniform(0,.1)
	v = random.uniform(0.95, 1)

	# Star Random Color Variation from Green :
	# White in HSV (0,0,1)
	#h = uniform(0.25, 0.38)
	#s = uniform(0.2, 1)
	#v = uniform(0.3, 1)

	r, g, b = hsv_to_rgb(h, s, v)

	for i in range(1,n_rotations):
		angle_step = float(delta_angle * i)
		angle = star_initial_angle[j] + angle_step
		step_x = star_r[j]*math.cos( angle )
		step_y = star_r[j]*math.sin( angle )
		star_x[j].append( rotational_axis_x + step_x)
		star_y[j].append( rotational_axis_y + step_y)

	# Plot Star Trail :
	#plt.plot(star_x[j], star_y[j], '.', markersize=star_size[-1],  alpha=star_alpha[-1], color=(r,g,b))
	plt.plot(star_x[j], star_y[j], '.', markersize = star_size[-1], markeredgewidth = star_size[-1], color=(r,g,b))

#--- Plot ---#

# Save Star Trail Plot :
print "Rendering Star Trail Figure : Star_Trails_"+date+".png\r"

# Remove Frame and Axes :
ax = star_trail.gca()
ax.set_frame_on(False)
ax.set_aspect('equal')	# Set equal aspect ratio
ax.set_xticks([])
ax.set_yticks([])
plt.axis('off')

# High Quality:
star_trail.savefig("Star_Trails_"+date+".png", dpi=1000, facecolor = bg, bbox_inches='tight', pad_inches=0)

# Fast, Low Quality :
#star_trail.savefig("Star_Trails_"+date+".png", facecolor='#152033', bbox_inches='tight', pad_inches=0)

#--- End of Script ---#
