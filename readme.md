# Projects

File : Projects/readme.md
Author : Greg Furlich

Comment : git repository to showcase fun coding projects of Greg Furlich

## Star Trails

StarTrails/StarTrail.py : A python script to create random star positions and a random rotational axis. Then rotate the stars around the axis to make star trails. A image is rendered from the star trails.

	Execution : ./StarTrails <n_stars> <rotation_angle>

	Outputs : Figures/Stars_Initial_v<YYYYMMDD_HHMMSS>.png
	Figures/Star_Trails_v<YYYYMMDD_HHMMSS>.png

![Star Trails Example Figure](https://github.com/gfurlich/Projects/blob/master/StarTrails/Figures/Star_Trails_example.png)

StarTrails/StarTrailMovement.py : A python script simulate star trails for a random array of <n_stars> around a randomly placed rotational axis for a length of a <rotation_angle>. Create figures of the rotations and combine into GIFs.

	Execution : ./StarTrailsMovement <n_stars> <rotation_angle>

	Outputs : Gif_Figures/Stars_Initial_<YYYYMMDD>.png
	Gif_Figures/Star_Trail_Movement_v<YYYYMMDD>/Stars_Trails_<IIII>.png
	GIFs/Star_Trail_v<YYYYMMDD>.gif

![Star Trail Movement Example GIF](https://github.com/gfurlich/Projects/blob/master/StarTrails/GIFs/Star_Trail_Movement_example.gif)
