#!/usr/bin/env python

# Copyright 2012 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from sys import argv
import numpy as np
import pyglet

class Layer:
	def __init__(self):
		self.moves = []

class Move:
	def __init__(self,orig,dest,extruding,tool):
		self.orig = np.array(orig)
		self.dest = np.array(dest)
		self.extruding = extruding
		self.tool = tool
	def __str__(self):
		return str(self.orig) + " " + str(self.dest)

class GCodeParser:
	def __init__(self):
		self.layers = []
		self.max = np.zeros(3)
		self.min = np.zeros(3)

	def parse(self,fid):
		self.layers.append(Layer())
		cur = np.zeros(3)
		nxt = np.zeros(3)
		tool = None
		for line in fid:
			#strip comments and split
			pieces = line.split(";")
			pieces = pieces[0].split()
			if len(pieces) < 1:
				continue
			if pieces[0] == "G92":
				for piece in pieces[1:]:
					piece.strip(";")
					if piece[0] == "X":
						cur[0] = float(piece[1:])
					elif piece[0] == "Y":
						cur[1] = float(piece[1:])
					elif piece[0] == "Z":
						cur[2] = float(piece[1:])
					if not piece[0] == "E":
						self.moves = []
						self.max = np.zeros(3)
						self.min = np.zeros(3)
						
			elif pieces[0] == "G1":
				#if not all coordinates are given, they stay the same
				nxt = cur.copy()
				extruding = False
				for piece in pieces[1:]:
					piece.strip(";")
					if piece[0] == "X":
						nxt[0] = float(piece[1:])
					elif piece[0] == "Y":
						nxt[1] = float(piece[1:])
					elif piece[0] == "Z":
						nxt[2] = float(piece[1:])
						if nxt[2] != cur[2]:
							self.layers.append(Layer())
					elif piece[0] == "E":
						extruding = True
				self.layers[-1].moves.append(Move(cur,nxt,extruding,tool))
				self.max = np.maximum(self.max, nxt)
				self.min = np.minimum(self.min, nxt)
				cur = nxt.copy()
			elif pieces[0] == "T0":
				tool = 0
			elif pieces[0] == "T1":
				tool = 1
				
		self.size = (self.max - self.min).max()

class MainWindow(pyglet.window.Window):
	def __init__(self,filename):
		pyglet.window.Window.__init__(self)

		self.parser = GCodeParser()
		fid = open(filename)
		self.parser.parse(fid)

		self.scale = 4
		size = int(self.scale*self.parser.size)
		self.set_size(size,size)

		self.current_layer = 0

		self.tool_colors = [(255,0,0),(0,255,0)]

		self.label = pyglet.text.Label("Layer: %d" % self.current_layer)

	def on_draw(self):
		self.clear()
		#draw paths
		moves = self.parser.layers[self.current_layer].moves
		for m in moves:
			coords = tuple((p[i] - self.parser.min[i])*self.scale for p in [m.orig,m.dest] for i in range(2))
			color = (255,255,255)
			if m.extruding:
				color = self.tool_colors[m.tool]
			colors = tuple(color[i] for j in range(2)  for i in range (3))
			pyglet.graphics.draw(2,pyglet.gl.GL_LINES,("v2f",coords),("c3B",colors))
		#draw stats
		self.label.draw()

	def _change_layer(self,change):
		self.current_layer += change
		self.current_layer = max(0,self.current_layer)
		self.current_layer = min(len(self.parser.layers)-1,self.current_layer)
		self.label.text = "Layer: %d" % self.current_layer

	def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
		self._change_layer(scroll_y)

	def on_key_press(self,symbol, mods):
		if symbol == pyglet.window.key.UP:
			self._change_layer(1)
		elif symbol == pyglet.window.key.DOWN:
			self._change_layer(-1)

if len(argv) > 1:
	win = MainWindow(argv[1])
	pyglet.app.run()
else:
	print "usage: pathetic.py filename"
