import tkinter as tk
import random
import math
from math import pi
from collections import namedtuple

def distance(point1, point2):
	x1,y1 = point1
	x2,y2 = point2
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def x_distance(x1, x2):
	# **2 and sqrt to ensure that the answer is positive
	return math.sqrt((x2-x1)**2)

def direction_vector(point1, point2):
	x1,y1 = point1
	x2,y2 = point2
	return (x2-x1, y2-y1)

def slope(point1, point2):
	x1,y1 = point1
	x2,y2 = point2
	if x1 == x2:
		m = 'None'
	else:
		m = (y2-y1)/(x2-x1)
	return m

def x_equals(line, b):
	'''
	Given a line(point1, point2, slope), and a y value
	the corresponding x is solved for such that the 
	given y and the x are on the line
	Note: a line is y-b = m(x-a)
	rewrite: a = (m(x)-y+b)/m
			 
	'''
	m = line.slope
	x,y = line.point1
	return ((m*x)-y+b)/m


class Chaos_Game(tk.Tk):
	def __init__(self, width=500, height=500):
		self.width = width
		self.height = height
		super().__init__()
		self.title('Chaos Game')
		self.canvas = Board(self, self.width, self.height)
		self.canvas.pack()
		#mainloop that runs the progame
		self.mainloop()



class Board(tk.Canvas):
	def __init__(self, master, width, height):
		self.master = master
		self.width = width
		self.height = height
		self.center = ((1/2)*self.width, (1/2)*self.height)
		self.scale= (1/2)
		super().__init__(self.master, width=self.width, height=self.height)
		self.shape = Geometric_Shape(self.center, (7/16)*self.width, 3)
		self.shape.draw_shape(self)
		#self.point will be updated as the simulation progresses
		self.point = self.shape.starting_point
		self.draw_point(self.point)
		self.colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'brown']
		self.update()


	def draw_point(self, center_point, color='black'):
		'''
		Given the center point, draw a tkinter oval
		'''
		x1, y1 = center_point
		self.create_oval(x1-1,y1-1,x1+1,y1+1, fill=color, outline=color)

	def update(self):
		'''
		Draw points randomly inside the triangle
		'''
		#gets a ramdom vertex from the shape
		vertex = self.shape.random_vertex()

		#find the direction vector between the two points
		dir_vector = direction_vector(self.point, vertex)
		
		#finds the distance between the vertex and the current self.point 
		#also known as magnitude
		d = distance(self.point, vertex)*self.scale
		
		#find the unit vector
		unit_vector = (dir_vector[0]/d, dir_vector[1]/d)
		
		scale = d*self.scale
		#set the new x and y coordinates
		new_x = unit_vector[0]*scale + self.point[0]
		new_y = unit_vector[1]*scale + self.point[1]
		color = random.choice(self.colors)
		self.draw_point((new_x, new_y), color)
		# #updates the current point
		self.point = ((new_x, new_y))
		self.id = self.master.after(50, self.update)


class Menu(tk.Canvas):
	def __init__(self, master, width, height):
		self.master = master
		self.width = width
		self.height = height
		super().__init__(self.master, width=self.width, height=self.height)


class Geometric_Shape():
	'''
	Given the center point, radius, and vertexes a geometric shape is created
	'''
	def __init__(self, center, radius, vertexes):
		self.center = center
		self.radius = radius
		self.vertexes = vertexes
		self.angle = 2*pi/vertexes
		self.points = self.get_points()
		self.lines = self.get_lines()
		self.starting_point = self.starting_point()

	def get_points(self):
		points = []
		for i in range(self.vertexes):
			#if the number of vertexes is even
			if self.vertexes%2 == 0:
				if self.vertexes == 4:
					#the angle is rotated by 45 degrees
					curr_angle = (i)*self.angle - math.radians(45)
				else:
					#the angle is not rotated
					curr_angle = (i)*self.angle
			else:
				#the angle is rotated by 90 degrees
				curr_angle = (i)*self.angle - math.radians(90)
			#the x value given the angle + the center offset
			x = (math.cos(curr_angle)*self.radius) + self.center[0]
			#the y value given the angle + the center offset 
			y = (math.sin(curr_angle)*self.radius) + self.center[1]
			points.append((x,y))
		return points

	def get_lines(self):
		Line = namedtuple('Line', 'point1 point2 slope')
		lines =[]
		for i,point in enumerate(self.points):
			#if it's not the last point
			if point != self.points[-1]:
				x1,y1 = point
				x2,y2 = self.points[i+1]
				m = slope((x1,y1),(x2,y2))
				lines.append(Line([x1,y1],[x2,y2],m))
			else:
				x1,y1 = point
				x2,y2 = self.points[0]
				m = slope((x1,y1),(x2,y2))
				lines.append(Line([x1,y1],[x2,y2],m))
		return lines

	def draw_shape(self, canvas):
		for i,point in enumerate(self.points):
			#if it's not the last point
			if point != self.points[-1]:
				x1,y1 = point
				x2,y2 = self.points[i+1]
				if i ==0:
					canvas.create_line(x1, y1, x2, y2, fill='red')
				else:
					canvas.create_line(x1, y1, x2, y2, fill='blue')
			else:
				x1,y1 = point
				x2,y2 = self.points[0]
				canvas.create_line(x1, y1, x2, y2, fill='green')

	def random_vertex(self):
		return random.choice(self.points)

	def starting_point(self):
		'''
		Randomly determins the starting point for the program
		'''
		found_point = False
		while not found_point:
			#determin how to check that the starting point is within the triangle
			#randomly choose a point from the circle that surrounds the figure
			x = random.randrange(round(self.center[0]-self.radius,0), round(self.center[0]+self.radius,0))
			y = random.randrange(round(self.center[1]-self.radius,0), round(self.center[1]+self.radius,0))
			point = (x,y)
			# import pdb; pdb.set_trace()
			if self.within_figure(point):
				found_point = True
		return point

	def within_figure(self, point):
		x,y = point
		print('Point: {}'.format(point))
		#check the y variable of the point to determin which lines 
		#the point is between. Either the y value is between the lines y's,
		#or the point is on a vertex
		between = []
		for line in self.lines:
			#not sure which y is larger
			if (line.point1[1] <= y <= line.point2[1]) or (line.point2[1] <= y <= line.point1[1]):
				between.append(line)
		#the point's y is bounded by the y's of the figure if between != []
		if between != []:
		#given the y, solve each line for x, which gives a line that is parallel to our random point
		#if the sum of the distance from the point to each line x is equal to the distance each line at the given y,
		#then the point is inside the shape.
			x_s = []
			for line in between:
				#line either has a slope
				if type(line.slope) == float:
					x_s.append(x_equals(line, y))
				#line has no slope
				elif line.slope == 'None':
					x_s.append(line.point1[0])
			#check if the distances add up
			if (x_distance(x_s[0], x)+x_distance(x_s[1], x) == x_distance(x_s[0], x_s[1])):
				return True
			else:
				return False
		else:
			return False






















