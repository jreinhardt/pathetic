========
Pathetic
========

Summary
=======

Pathetic is a very simple viewer for RepRap [#reprap]_ GCode [#gcode]_ written
in python [#python]_, using numpy [#numpy]_ and pyglet [#pyglet]_. It is also
an opportunity for me to learn a bit OpenGL.

Usage
=====

Pathetic is started from the commandline with the name of the GCode file as
first argument.

One can change between the layer using the arrow keys or a mousewheel.

Non-extruding moves are shown white, primary extruder red, secondary extruder
green.

Ideas for Features
==================

This does neither mean that I will implement any of this nor that these are
good ideas. They are just ideas and I wanted to write them down somewhere.

* 3D View
* Statistics (Layer statistics)
* Coloring assistant (visual selection of parts, output of filament length to fuse)
* Comparison Window (to compare Skeinforge [#skeinforge]_ and Slic3r [#slic3r]_ output)
* GCode Debug/Polish Mode (Graphical way to edit GCode, to remove unwanted paths, infill, ...)


Roadmap
=======

These are things that I really want to implement in foreseeable future.

* Scale (cm, inch, mm)
* Zoom

.. [#reprap] http://reprap.org/wiki/Main_Page
.. [#gcode] http://reprap.org/wiki/GCode
.. [#python] http://python.org/
.. [#numpy] http://numpy.scipy.org/
.. [#pyglet] http://pyglet.org
.. [#skeinforge] http://fabmetheus.crsndoo.com/
.. [#slic3r] http://slic3r.org/



