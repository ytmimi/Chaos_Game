import tkinter as tk
import sys
import random
import math
from math import pi
from collections import namedtuple
from PIL import Image, ImageGrab


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
		self.board.grid(row=1, column=0, sticky=tk.E+tk.S+tk.N+tk.W)
		#shape_menu
		self.shape_menu = Shape_Menu(self, (1/4)*self.width, self.height)
		# self.shape_menu.pack(side=tk.LEFT)
		self.shape_menu.grid(row=1, column=1, sticky=tk.E+tk.N+tk.S)

		#add a menu
		self.main_menu = Main_Menu(self)
		self.config(menu=self.main_menu)

		#add a toolbar
		self.toolbar = Tool_Bar(self)
		# self.toolbar.pack(side=tk.TOP)
		self.toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.E+tk.W)

		#mainloop that runs the progame				
		self.mainloop()


	def new_shape(self):
		self.board.create_shape()
	
	def start(self):
		self.board.update()
		
	def pause(self):
		self.board.pause_unpause()

	def clear(self):
		self.board.cancel_update()
		self.board.remove_shape()
		self.board.unpause()

	def screen_shot(self):
		board_x = self.board.winfo_rootx()
		board_y =  self.board.winfo_rooty()
		board_width = self.board.winfo_width()
		board_height = self.board.winfo_height()
		#for some reason the resolution on ImageGrab is 2X the resolution of my screen
		image = ImageGrab.grab((2*board_x, 2*board_y, 2*(board_x+board_width), 2*(board_y+board_height)))
		image.show()

	def close(self):
		sys.exit()

	def get_x(self):
		return self.shape_menu.x_input.get_value()

	def get_y(self):
		return self.shape_menu.y_input.get_value()

	def get_board_center(self):
		return self.board.center

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
		if len(self.board.shapes) >0:
			#add a way to change the color
			l_color = self.get_line_color()
			for shape in self.board.shapes:
				shape.draw_shape(self.board, l_color)

	def hide_shape_outline(self):
		if len(self.board.shapes) > 0:
			for shape in self.board.shapes:
				shape.hide_shape(self.board)

	def shape_checkbox(self):
		self.shape_menu.show_line
		return self.shape_menu.show_line.get() == 1

	def get_rotation(self):
		return self.shape_menu.rotation_slider.get()
		



class Tool_Bar(tk.Frame):
	def __init__(self, master):
		self.master = master
		super().__init__(master)
		self.config(bd=5, relief=tk.GROOVE)
		self.new_shape_btn = tk.Button(self, text='New Shape', command= lambda: self.master.new_shape())
		self.new_shape_btn.pack(side=tk.LEFT, padx=5,)
		self.start_btn = tk.Button(self, text='Start', command= lambda: self.master.start())
		self.start_btn.pack(side=tk.LEFT, padx=5,)
		self.pause_unpause_btn = tk.Button(self, text='Pause/unpause', command= lambda: self.master.pause())
		self.pause_unpause_btn.pack(side=tk.LEFT, padx=5,)
		self.clear_btn = tk.Button(self, text='Clear', command = lambda: self.master.clear())
		self.clear_btn.pack(side=tk.LEFT, padx=5,)
		self.screen_shot_btn = tk.Button(self, text='Capture Image', command = lambda: self.master.screen_shot())
		self.screen_shot_btn.pack(side=tk.LEFT, padx=5,)
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
		self.bind('<Button-2>', self.click_set_color)
		self.bind('<Button-1>', self.board_info)
		self.bind('<B1-Motion>', self.move_shape)
		self.bind('<Double-Button-1>', self.select_shape)
		self.pause = False
		self.id = None
		self.mouse_x = None
		self.mouse_y = None

	def create_shape(self, ):
		'''
		Creates the Geometric shape object, draws it, and then adds the shape to the shapes list
		'''
		# if self.shapes == []:
		#get the x and y
		x_val = self.master.get_x()
		y_val = self.master.get_y()
		#get the number of vertexes
		vertexes = self.master.get_vertex()
		#get the scale
		scale = self.master.get_rate()
		#ge the radius of the figure
		radius = self.master.get_shape_radius()
		#get the point color
		p_color = self.master.get_point_color()
		#get the point size
		p_size = self.master.get_point_size()
		#get the line color
		l_color = self.master.get_line_color()
		#get the rotation
		rotation = self.master.get_rotation()

		if vertexes >=3 and scale !=0 :
			#draw the shape
			shape = Geometric_Shape((x_val, y_val), radius, vertexes, scale, p_color, p_size, rotation)
			if self.master.shape_checkbox():
				shape.draw_shape(self, l_color)
			self.shapes.append(shape)

	def remove_shape(self):
		'''
		Removes the shape from the shapes list and clears the board
		'''
		while len(self.shapes) != 0:
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
		if (len(self.shapes) >0) and (not self.pause):
			for shape in self.shapes:
				shape.update(self)
			self.id = self.master.after(100, self.update)

	def click_set_color(self, event):
		x = event.x
		y = event.y
		if len(self.shapes) >0: 
			for shape in self.shapes:
				if shape.within_figure((x,y)):
					color = self.master.get_point_color()
					shape.set_color(color)

	def pause_unpause(self):
		'''Used to toggle between paused and unpaused'''
		if len(self.shapes) >= 1:
			if not self.pause:
				self.pause = True
			else:
				self.pause = False
				self.update()

	def unpause(self):
		'''Used to reset the pause'''
		self.pause = False

	def cancel_update(self):
		if self.id != None:
			self.after_cancel(self.id)
		self.id = None

	def board_info(self, event):
		self.mouse_x = event.x
		self.mouse_y = event.y
		

	def select_shape(self, event):
		#double click event
		print('hey')

	def move_shape(self, event):
		self.pause = True
		x = event.x
		y = event.y
		point = (x,y)
		dir_vector = direction_vector((self.mouse_x, self.mouse_y), point)
		for shape in self.shapes:
			if shape.within_figure(point):
				shape.move_shape(self, dir_vector)
		#set the new x and y mouse position
		self.mouse_x = x
		self.mouse_y = y





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
		#set the x and y positions
		self.x_lbl = self.create_label((1/8)*self.width, 25, 'X:')
		self.x_input = self.create_input_fld((5/8)*self.width, 25, self.master.get_board_center()[0])

		self.y_lbl = self.create_label((1/8)*self.width, 75, 'Y:')
		self.y_input = self.create_input_fld((5/8)*self.width, 75, self.master.get_board_center()[1])

		#set the number of vertexes
		self.vertex_lbl = self.create_label((1/2)*self.width, 100, 'Vertexes')
		self.vertex_input = self.create_input_fld((1/2)*self.width, 125, 3)

		#set the size of the shape
		self.radius_lbl = self.create_label((1/2)*self.width, 150, 'Radius')
		self.radius_input = self.create_input_fld((1/2)*self.width, 175, 150)

		#set the scale of the moving point
		self.rate_lbl = self.create_label((1/2)*self.width, 200, 'Scale')
		self.rate_input = self.create_input_fld((1/2)*self.width, 225, .5)

		#set the size of the point
		self.size_lbl = self.create_label((1/2)*self.width, 250, 'Point Size')
		self.size_input = self.create_input_fld((1/2)*self.width, 275, 1)

		#set the color of the point
		self.point_color_lbl = self.create_label((1/2)*self.width, 300, 'Point Color')
		self.point_color_mnu = self.create_opt_mnu((1/2)*self.width, 325,'black', ['black', 'blue', 'red', 'green', 'orange', 'purple', 'yellow', 'brown', 'rainbow'])
		
		#Set the line color and toggle the line visibility
		self.line_color_lbl = self.create_label((1/2)*self.width,350, 'Line Color')
		self.line_color_mnu = self.create_opt_mnu((1/2)*self.width,375,'black',['black', 'blue', 'red', 'green', 'orange', 'purple', 'yellow', 'brown'] )

		#adds the checkbox for displaying the shapes line
		self.line_cbox = self.create_checkbox((1/2)*self.width,400, 'Show Line', self.toggle_shape_line)
		
		#Sets the rotation slider
		self.rotation_lbl = self.create_label((1/2)*self.width, 450, 'Rotation')
		self.rotation_slider = self.create_slider((1/2)*self.width, 475, 0, 360 )


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

	def create_slider(self, x1, y1, min_, max_):
		slider = tk.Scale(self, from_ = min_, to = max_ )
		slider.config(orient=tk.HORIZONTAL)
		self.create_window(x1, y1, window = slider)
		return slider



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

	def set_vale(self, val):
		self.set(val)




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
	def __init__(self, center, radius, vertexes, scale, point_color, point_size, rotation=0):
		self.center = center
		self.radius = radius
		self.vertexes = vertexes
		self.angle = 2*pi/self.vertexes
		self.rotation = math.radians(rotation)
		self.points = self.get_points()
		self.lines = self.get_lines()
		self.starting_point = self.starting_point()
		self.scale = scale
		self.point_color = point_color
		self.point_size = point_size
		self.dot_list = []
		self.line_ids = []
		

	def get_points(self):
		points = []
		for i in range(int(self.vertexes)):
			#if the number of vertexes is even
			if self.vertexes%2 == 0:
				if self.vertexes == 4:
					#the angle is rotated by 45 degrees
					curr_angle = (i)*self.angle - math.radians(45) + self.rotation
				else:
					#the angle is not rotated
					curr_angle = (i)*self.angle + self.rotation
			else:
				#the angle is rotated by 90 degrees
				curr_angle = (i)*self.angle - math.radians(90) + self.rotation

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
			self.line_ids.append(line_id)


	def hide_shape(self,canvas):
		while len(self.line_ids) > 0:
			self.line_ids.remove(self.line_ids[0])
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
		self.point_color = color


	def create_dot(self, canvas, color):
		dot = Dot(self.starting_point[0], self.starting_point[1], self.point_size, color)	
		if dot not in self.dot_list:
			dot.draw_dot(canvas)
			self.dot_list.append(dot)

	def update(self, canvas):
		'''
		Draw points randomly inside the figure
		'''
		#gets a ramdom vertex, the position of the point, and the scale from the shape
		vertex = self.random_vertex()
		point = self.starting_point
		scale = self.scale

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
		if self.point_color == 'rainbow':
			color = canvas.master.random_point_color()
			self.create_dot(canvas, color)
			# self.draw_point((new_x, new_y), color, self.point_size)
		else:
			self.create_dot(canvas, self.point_color)
			# self.draw_point((new_x, new_y), shape.color, self.point_size)
		# #updates the current point
		self.update_point(new_x, new_y)

	#code to move the shape on the screen
	def move_shape(self, canvas, offset):
		#move the vertexes
		for i, point in enumerate(self.points):
			self.points[i] = (point[0]+ offset[0], point[1]+ offset[1])
			

		#move the lines:
		for line in self.lines:
			line.point1[0] = line.point1[0]+ offset[0]
			line.point1[1] = line.point1[1]+ offset[1]
			line.point2[0] = line.point2[0]+ offset[0]
			line.point2[1] = line.point2[1]+ offset[1]

		#move the starting point
		self.starting_point = (self.starting_point[0] + offset[0], self.starting_point[1] + offset[1])

		#move the lines on the screen
		for id_ in self.line_ids:
			canvas.move(id_, offset[0], offset[1])

		#move the center point
		self.center = (self.center[0] + offset[0], self.center[1] + offset[1])
		
		#move the dots
		for dot in self.dot_list:
			canvas.move(dot.dot, offset[0], offset[1])
		
		



class Dot():
	def __init__(self, x, y, size, color):
		self.x = x
		self.y = y
		self.size = size
		self.color = color

	def draw_dot(self, canvas):
		'''
		Draws the dot on the canvas
		'''
		self.dot = canvas.create_oval(self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size, 
							fill=self.color, outline=self.color, tags='dot')

	#functions to rotate the dot
	def rotate_dot(self):
		pass

class Image_Capture():
	pass























