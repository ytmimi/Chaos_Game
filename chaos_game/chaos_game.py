import tkinter as tk
import sys
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
		
		#board
		self.board = Board(self, self.width, self.height)
		# self.board.pack(side=tk.LEFT)
		self.board.grid(row=1, column=0)
		#shape_menu
		self.shape_menu = Shape_Menu(self, (1/4)*self.width, self.height)
		# self.shape_menu.pack(side=tk.LEFT)
		self.shape_menu.grid(row=1, column=1)


		#add a menu
		self.main_menu = Main_Menu(self)
		self.config(menu=self.main_menu)

		#add a toolbar
		self.toolbar = Tool_Bar(self)
		# self.toolbar.pack(side=tk.TOP)
		self.toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.E+tk.W)

		#mainloop that runs the progame				
		self.mainloop()


	def start(self):
		if len(self.board.shapes) < 1:
			self.board.point_size = self.get_point_size()
		self.board.create_shape()


	def pause(self):
		self.board.pause_unpause()

	def clear(self):
		self.board.remove_shape()
		self.board.unpause()

	def close(self):
		sys.exit()


	def get_point_color(self):
		return self.shape_menu.point_color_mnu.get_value()

	def random_point_color(self):
		return random.choice(self.shape_menu.point_color_mnu.options[1:-1])

	def get_line_color(self):
		return self.shape_menu.line_color_mnu.get_value()

	def random_line_color(self):
		return random.choice(self.shape_menu.line_color_mnu.options)

	def get_vertex(self):
		return self.shape_menu.vertex_input.get_value()

	def get_rate(self):
		return self.shape_menu.rate_input.get_value()

	def get_point_size(self):
		return self.shape_menu.size_input.get_value()

	def get_shape_radius(self):
		return self.shape_menu.radius_input.get_value()

	def show_shape_outline(self):
		if self.board.shapes != []:
			#add a way to change the color
			l_color = self.get_line_color()
			self.board.shapes[0].draw_shape(self.board, l_color)

	def hide_shape_outline(self):
		if self.board.shapes != []:
			self.board.shapes[0].hide_shape(self.board)

	def shape_checkbox(self):
		self.shape_menu.show_line
		return self.shape_menu.show_line.get() == 1
		



class Tool_Bar(tk.Frame):
	def __init__(self, master):
		self.master = master
		super().__init__(master)
		self.config(bd=5, relief=tk.GROOVE)
		self.start_btn = tk.Button(self, text='Start', command= lambda: self.master.start())
		self.start_btn.pack(side=tk.LEFT, padx=5,)
		self.pause_unpause_btn = tk.Button(self, text='Pause/unpause', command= lambda: self.master.pause())
		self.pause_unpause_btn.pack(side=tk.LEFT, padx=5,)
		self.clear_btn = tk.Button(self, text='Clear', command = lambda: self.master.clear())
		self.clear_btn.pack(side=tk.LEFT, padx=5,)
		self.close_btn = tk.Button(self, text='Close', comman= lambda: self.master.close())
		self.close_btn.pack(side=tk.LEFT, padx=5,)





class Main_Menu(tk.Menu):
	def __init__(self, master):
		self.master = master
		super().__init__(master)
		self.file_menu = File_Menu(self, 'File')
		self.add_cascade(label=self.file_menu.label, menu=self.file_menu)


class File_Menu(tk.Menu):
	def __init__(self, master, label):
		self.master = master
		self.root = self.master.master
		self.label = label
		super().__init__(master, tearoff=0)
		#add things that the file menu can do:
		self.add_command(label='New Shape...', command=self.print_hello)

	def print_hello(self):
		print('hello')





class Board(tk.Canvas):
	def __init__(self, master, width, height):
		self.master = master
		self.width = width
		self.height = height
		self.center = ((1/2)*self.width, (1/2)*self.height)
		super().__init__(self.master, width=self.width, height=self.height)
		self.shapes = []
		self.bind('<Button-1>', self.click_set_color)
		self.pause = False
		self.point_size = 1
		

	def create_shape(self, ):
		'''
		Creates the Geometric shape object, draws it, and then adds the shape to the shapes list
		'''
		if self.shapes == []:
			#get the number of vertexes
			vertexes = self.master.get_vertex()
			#get the scale
			scale = self.master.get_rate()
			#ge the radius of the figure
			radius = self.master.get_shape_radius()
			#get the point color
			p_color = self.master.get_point_color()
			#get the line color
			l_color = self.master.get_line_color()

			if vertexes >=3 and scale !=0 :
				#draw the shape
				shape = Geometric_Shape(self.center, radius, vertexes, scale, p_color)
				if self.master.shape_checkbox():
					shape.draw_shape(self, l_color)
				self.shapes.append(shape)
				self.update()

	def remove_shape(self):
		'''
		Removes the shape from the shapes list and clears the board
		'''
		self.shapes.remove(self.shapes[0])
		self.delete("all")


	def draw_point(self, center_point, color='black', size=1):
		'''
		Given the center point, draw a tkinter oval
		'''
		x1, y1 = center_point
		self.create_oval(x1-size,y1-size,x1+size,y1+size, fill=color, outline=color)

	def update(self):
		'''
		Draw points randomly inside the triangle
		'''
		if (self.shapes != []) and (not self.pause):
			#gets a ramdom vertex, the position of the point, and the scale from the shape
			vertex = self.shapes[0].random_vertex()
			point = self.shapes[0].starting_point
			scale = self.shapes[0].scale

			#find the direction vector between the two points
			dir_vector = direction_vector(point, vertex)
			
			#finds the distance between the vertex and the current self.point 
			#also known as magnitude
			d = distance(point, vertex)
			
			#find the unit vector
			unit_vector = (dir_vector[0]/d, dir_vector[1]/d)
			
			scale = d*scale
			#set the new x and y coordinates
			new_x = unit_vector[0]*scale + point[0]
			new_y = unit_vector[1]*scale + point[1]
			#draw the new point
			if self.shapes[0].color == 'rainbow':
				color = self.master.random_point_color()
				self.draw_point((new_x, new_y), color, self.point_size)
			else:
				self.draw_point((new_x, new_y), self.shapes[0].color, self.point_size)
			# #updates the current point
			self.shapes[0].update_point(new_x, new_y)
			self.id = self.master.after(50, self.update)

	def click_set_color(self, event):
		x = event.x
		y = event.y

		if self.shapes != [] and self.shapes[0].within_figure((x,y)):
			color = self.master.get_point_color()
			self.shapes[0].set_color(color)

	def pause_unpause(self):
		'''Used to toggle between paused and unpaused'''
		if self.shapes != []:
			if not self.pause:
				self.pause = True
			else:
				self.pause = False
				self.update()

	def unpause(self):
		'''Used to reset the pause'''
		self.pause = False




class Shape_Menu(tk.Canvas):
	def __init__(self, master, width, height):
		self.master = master
		self.width = width
		self.height = height
		self.show_line = tk.IntVar()
		super().__init__(self.master, width=self.width, height=self.height)
		self.config(bd=3, relief=tk.GROOVE)
		# self.start_btn = self.create_button((1/2)*self.width, self.height-175, 'Start', self.master.start,)
		# self.pause_btn = self.create_button((1/2)*self.width, self.height-125, 'Pause/Play', self.master.pause,)
		# self.clear_btn = self.create_button((1/2)*self.width, self.height-75, 'Clear', self.master.clear,)
		# self.close_btn = self.create_button((1/2)*self.width, self.height-25, 'Close', self.master.close)
		#set the number of vertexes
		self.vertex_lbl = self.create_label((1/2)*self.width, 25, 'Vertexes')
		self.vertex_input = self.create_input_fld((1/2)*self.width, 50, 3)

		#set the size of the shape
		self.radius_lbl = self.create_label((1/2)*self.width, 75, 'Radius')
		self.radius_input = self.create_input_fld((1/2)*self.width, 100, 150)

		#set the scale of the moving point
		self.rate_lbl = self.create_label((1/2)*self.width, 125, 'Scale')
		self.rate_input = self.create_input_fld((1/2)*self.width, 150, .5)

		#set the size of the point
		self.size_lbl = self.create_label((1/2)*self.width, 175, 'Point Size')
		self.size_input = self.create_input_fld((1/2)*self.width, 200, 1)

		#set the color of the point
		self.point_color_lbl = self.create_label((1/2)*self.width, 250, 'Point Color')
		self.point_color_mnu = self.create_opt_mnu((1/2)*self.width, 275,'black', ['black', 'blue', 'red', 'green', 'orange', 'purple', 'yellow', 'brown', 'rainbow'])
		
		#Set the line color and toggle the line visibility
		self.line_color_lbl = self.create_label((1/2)*self.width,325, 'Line Color')
		self.line_color_mnu = self.create_opt_mnu((1/2)*self.width,350,'black',['black', 'blue', 'red', 'green', 'orange', 'purple', 'yellow', 'brown'] )

		self.line_cbox = self.create_checkbox((1/2)*self.width,375, 'Show Line', self.toggle_shape_line)
		# self.show_line_btn = self.create_button((1/2)*self.width,325, 'Show Outline', self.master.show_shape_outline)
		# self.hide_line_btn = self.create_button((1/2)*self.width,325, 'Hide Outline', self.master.hide_shape_outline)


	def create_button(self,x1, y1, text, func, *args):
		button = tk.Button(self, text=text, command= lambda: func(*args))
		button.config(relief=tk.GROOVE)
		self.create_window(x1,y1, window=button)
		return button

	def create_label(self, x1,y1, text):
		label = tk.Label(self, text=text)
		self.create_window(x1, y1, window=label)
		return label

	def create_opt_mnu(self, x1, y1, default, option_list):
		menu = Option_Menu(self, default, option_list)
		self.create_window(x1, y1, window=menu)
		return menu

	def create_input_fld(self, x1, y1, default=''):
		input_fld = Input_Feild(self)
		input_fld.insert(0, default)
		self.create_window(x1, y1, window=input_fld)
		return input_fld


	def create_checkbox(self, x1, y1, text, func, *args):
		check_box = tk.Checkbutton(self, text="Show Line", variable=self.show_line, 
			onvalue=1, offvalue=0, command=lambda: func(*args), state=tk.ACTIVE)
		check_box.select()
		self.create_window(x1, y1, window=check_box)
		return check_box

	def toggle_shape_line(self):
		value = self.show_line.get()
		if value == 1:
			self.master.show_shape_outline()
		elif value == 0:
			self.master.hide_shape_outline()



class Input_Feild(tk.Entry):
	def __init__(self, master):
		self.master = master
		super().__init__(master)
		self.config(width=10)

	def get_value(self):
		try:
			val = self.get()
			if val != '':
				val = float(self.get())
			else:
				val = 0
		except Exception as e:
			raise e
		return val




class Option_Menu(tk.OptionMenu):
	def __init__(self, master, default, option_list):
		self.var = tk.StringVar()
		self.default = default
		self.var.set(self.default)
		self.options = option_list
		self.master = master
		super().__init__(self.master, self.var, *self.options)

	def get_value(self):
		val = self.var.get().split(' ')[-1]
		return val

	def get_default_value(self):
		val = self.default.split(' ')[-1]
		return val




class Geometric_Shape():
	'''
	Given the center point, radius, and vertexes a geometric shape is created
	'''
	def __init__(self, center, radius, vertexes, scale, color):
		self.center = center
		self.radius = radius
		self.vertexes = vertexes
		self.angle = 2*pi/self.vertexes
		self.points = self.get_points()
		self.lines = self.get_lines()
		self.starting_point = self.starting_point()
		self.scale = scale
		self.color = color

	def get_points(self):
		points = []
		for i in range(int(self.vertexes)):
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

	def update_point(self, x, y):
		self.starting_point = (x,y)


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

	def draw_shape(self, canvas, fill='black'):
		for i,point in enumerate(self.points):
			#if it's not the last point
			if point != self.points[-1]:
				x1,y1 = point
				x2,y2 = self.points[i+1]
				if i ==0:
					line_id = canvas.create_line(x1, y1, x2, y2, fill=fill, tags='line')
				else:
					line_id = canvas.create_line(x1, y1, x2, y2, fill=fill, tags='line')
			else:
				x1,y1 = point
				x2,y2 = self.points[0]
				line_id = canvas.create_line(x1, y1, x2, y2, fill=fill, tags = 'line')


	def hide_shape(self,canvas):
		canvas.delete('line')


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

	def set_color(self, color):
		self.color = color























