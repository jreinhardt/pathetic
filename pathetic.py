#!/usr/bin/env python
from sys import argv
import numpy as np
import pyglet
from pyglet.gl import *

class Layer:
	def __init__(self):
		self.moves = []

class Move:
	def __init__(self,orig,dest,extruding):
		self.orig = np.array(orig)
		self.dest = np.array(dest)
		self.extruding = extruding
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
				self.layers[-1].moves.append(Move(cur,nxt,extruding))
				self.max = np.maximum(self.max, nxt)
				self.min = np.minimum(self.min, nxt)
				cur = nxt.copy()
		self.size = (self.max - self.min).max()

class MainWindow(pyglet.window.Window):
	def __init__(self,filename):
		pyglet.window.Window.__init__(self)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluOrtho2D(0, self.width, 0, self.height)

		self.parser = GCodeParser()
		fid = open(filename)
		self.parser.parse(fid)

		self.scale = 4
		size = int(self.scale*self.parser.size)
		self.set_size(size,size)

		self.current_layer = 0

	def on_draw(self):
		self.clear()
		moves = self.parser.layers[self.current_layer].moves
		color = [255,255,255]
		for m in moves:
			coords = tuple((p[i] - self.parser.min[i])*self.scale for p in [m.orig,m.dest] for i in range(2))
			color = (255,255,255)
			if m.extruding:
				color = (255,0,0)
			colors = tuple(color[i] for j in range(2)  for i in range (3))
			pyglet.graphics.draw(2,pyglet.gl.GL_LINES,("v2f",coords),("c3B",colors))

	def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
		self.current_layer += scroll_y
		self.current_layer = max(0,self.current_layer)
		self.current_layer = min(len(self.parser.layers)-1,self.current_layer)

if len(argv) > 1:
	win = MainWindow(argv[1])
	pyglet.app.run()
else:
	print "usage: pathetic filename"
