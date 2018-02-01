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



		#mainloop
		self.mainloop()




class Board(tk.Canvas):
	def __init__(self, master, width, height):
		self.master = master
		self.width = width
		self.height = height
		super().__init__(self.master, width=self.width, height=self.height)




	def draw_triangle(self, point1, point2, point3):
		'''
		Each point should be a touple in the form (x,y) denoting the 
		vertex of a triangle
		'''



		self.create_line()








