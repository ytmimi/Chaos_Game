import tkinter as tk
import random

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
		#self.point will be updated as the simulation progresses
		self.point = self.starting_point()
		super().__init__(self.master, width=self.width, height=self.height)
		self.shape = Triangle(((1/2)*self.width,10), (10,self.height),(self.width-10,self.height))
		self.draw_triangle(self.shape)
		self.update()


	def starting_point(self):
		'''
		Randomly determins the starting point for the program
		'''
		#determin how to check that the starting point is within the triangle
		return (200, 450)
		

	def draw_triangle(self, triangle):
		'''
		Each point should be a touple in the form (x,y) denoting the 
		vertex of a triangle
		'''
		x1,y1 = triangle.point1 #top point
		x2,y2 = triangle.point2 #bottom left
		x3,y3 = triangle.point3 #bottom right
		self.create_line(x1,y1,x2,y2, fill='red')
		self.create_line(x2,y2,x3,y3, fill='blue')
		self.create_line(x3,y3,x1,y1, fill='green')

	def draw_point(self, center_point):
		'''
		Given the center point, draw a tkinter oval
		'''
		x1, y1 = center_point
		self.create_oval()

	def update(self):
		'''
		Draw points randomly inside the triangle
		'''
		pass



class Triangle():
	'''
	A class that defines a triangle
	'''
	def __init__(self, point1, point2, point3):
		self.point1 = point1
		self.x1, self.y1 = point1
		self.point2 = point2
		self.x2, self.y2 = point2
		self.point3 = point3
		self.x3, self.y3 = point3







