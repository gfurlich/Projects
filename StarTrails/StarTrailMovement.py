#!/usr/bin/env python
'''
File : StarTrailMovement.py
Author : Greg Furlich
Date Created : 12/21/2017

Purpose : Simulate Star Trails for a random array of nstars around a randomly placed rotational axis for a length of a angle. Create figures of the rotations and combine into GIFs.

Execution : ./StarTrailMovement.py <n_stars> <rotation_angle>

Example Execution : ./StarTrailMovement.py 20 30

'''

#--- Start of Script ---#

#--- Importing Python Modules ---#

import sys
import random
from matplotlib import pyplot as plt
import time
import math
from colorsys import hsv_to_rgb
import os, errno
import imageio

#--- Initial Parameters ---#

t_start = time.time()

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
rotation_angle = float(sys.argv[2]) * pi / 180

# Steps of Rotation :
n_rotations = 400

# Angle Steps :
delta_angle = rotation_angle / n_rotations 

#--- Star Initial Positions ---#
#print 'Star Initial Positions :'

# Preallocate Lists :
star_x = [[] for _ in xrange(n_stars)]	# stars x position nested list
star_y = [[] for _ in xrange(n_stars)]	# stars y position nested list

star_initial_x =  []	# stars x position list
star_initial_y =  []	# stars y position list

# Randomly Defining Stars Position :
for i in range(0,n_stars):
	star_initial_x.append(random.uniform(-1.1 * w, 1.1 * w))
	star_initial_y.append(random.uniform(-1.1 * h, 1.1 * h))

	#print 'Star '+str(i+1)+' (star_x, star_y) = \t('+str(star_initial_x[i])+','+str(star_initial_y[i])+')'

# Defining Random Rotational Axis :
rotational_axis_x = random.uniform(0,w)
rotational_axis_y = random.uniform(0,h)

#--- Plot Initial Star and Rotational Positions ---#

plt.figure(1)		# Initialize First Plot

# Legend Labes :
star_label = 'n_stars = '+str(n_stars)
rotation_label = 'Axis of Rotation, rotate = '+str(sys.argv[2])

plt.plot(star_initial_x, star_initial_y, '*', label = star_label)	# Star Plot
plt.plot(rotational_axis_x, rotational_axis_y, 'o',label = rotation_label)			# Rotation Axis Plot

plt.xlim([0,w])		# X Range
plt.ylim([0,h])		# Y Range

plt.legend(loc='upper left')

print "Rendering Initial Figure : Gif_Figures/Stars_Initial_"+date+".png"

plt.savefig("Figures/Stars_Initial_"+date+".png")	# Save Plot

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
	#print 'Star '+str(i+1)+' (Radial Dist, angle) = \t('+str(star_r[i])+', '+str(star_initial_angle[i])+')'

# Initialize Star Trail Plot :
star_trail = plt.figure(2, frameon=False)	

plt.xlim([0,w])		# X Range
plt.ylim([0,h])		# Y Range

# Calculate Star Rotation :
for i in range(1,n_rotations):

	print 'Calculating Rotation {:04d} / {:d} \r'.format(i+1,n_rotations),

	for j in range(0,n_stars):

		angle_step = float(delta_angle * i)
		angle = star_initial_angle[j] + angle_step
		step_x = star_r[j]*math.cos( angle )
		step_y = star_r[j]*math.sin( angle )
		star_x[j].append( rotational_axis_x + step_x)
		star_y[j].append( rotational_axis_y + step_y)


#--- Plot Star Trails ---#

# List for Star Size, Alpha, and Color:
star_size = []
star_color_r = []
star_color_g = []
star_color_b = []
star_alpha = []

# Randomize Star Attributes :
print '\nAssigning Randomize Star Attributes...'
for j in range(0,n_stars):


	# Star Random Size and Alpha :

	# Uniform Distribution Sampling :
	#star_size.append(float(random.uniform(.001,1)))
	#star_alpha.append(float(random.uniform(.5,1)))

	# Gaussian Distribution Sampling :
	#star_size.append(float(random.gauss(.01,.1) ) )
	star_alpha.append( random.betavariate(2,15) )

	# Beta Distribution Sampling 
	# (0 - 1 skewed distribution towards 0):
	star_size.append( random.betavariate(2,4) )	

	# Star Random Color Variation from White :
	# White in HSV (0,0,1)
	if ( j % 50 == 0 ) :
		h = random.uniform(0, 1) 	# Hue
		s = random.uniform(0, 1)	# Saturation
		v = random.uniform(0, 1)	# Value

	else :
		h = random.uniform(0, 1) 		# Hue
		s = random.betavariate(1, 15)		# Saturation
		v = 1 -  random.betavariate(1, 15)	# Value

	#print h, s, v

	# Conver HSV to RGB
	r, g, b = hsv_to_rgb(h, s, v)

	star_color_r.append(r)
	star_color_g.append(g)
	star_color_b.append(b)
		

# Plot Star Trail :
# with transparent background
for i in range(1,n_rotations-1):

	t_render_start = time.time()

	for j in range(0,n_stars):

		plt.plot(star_x[j][i], star_y[j][i], '.', markersize = star_size[j], markeredgewidth = star_size[j], alpha=star_alpha[j], color=(star_color_r[j],star_color_g[j],star_color_b[j]))

	# Remove Plot Frame and Axes :
	ax = star_trail.gca()
	ax.set_frame_on(False)
	ax.set_aspect('equal')	# Set equal aspect ratio
	ax.set_xticks([])
	ax.set_yticks([])
	plt.axis('off')

	# Save Figure Title :
	out_dir = "Gif_Figures/Star_Trail_Movement_%s/" % (date,)
	out_fig = out_dir+"Star_Trails_%04d.png" % (i,)

	# Create Directory for Out Figures :
	try:
    		os.makedirs(out_dir)
	except OSError as e:
    		if e.errno != errno.EEXIST:
       			raise

	#print out_fiG

	# Save Plot :
	#star_trail.savefig(out_fig, dpi=300, facecolor = background_color, bbox_inches='tight', pad_inches=0)
	star_trail.savefig(out_fig, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0)

	# Clear Figure
	#plt.clf()
	t_render_elapsed = time.time() - t_render_start

	print 'Rendering Rotation {:04d} / {:d} \t {:f} secs\r' %(i,n_rotations,t_render_elapsed),

#--- Create Background ---#


# Background colors for the sky:
#background_color = '#000814'

#out_background = out_dir+"Star_Background.png"

#os.system('convert -size %ix%i xc:%s %s' % (w, h, background_color, out_background,)

#--- Create GIF ---#

# Define GIF Name :
out_gif = 'GIFs/Star_Trail_Movement_%s.gif' % (date,)

print "Rendering GIF : "+out_gif

# Use ImageMagick and System commands:
os.system('convert '+out_dir+'Star_Trails_*.png '+out_gif)

# Add Background :
os.system('convert '+out_gif+' -coalesce   -background xc:'+background_color+' -alpha remove -layers Optimize '+out_gif[:-4]+'_w_bg.gif')

# GIF Size :
gif_size = subprocess.check_output('du -sh '+out_gif)
print 'GIF Size : %s' % (gif_size,)

#--- Time Elapsed ---#

# Total time elapsed :
t_total = time.time() - t_start

print 'total time : %f secs' % (t_total,)

#--- End of Script ---#
