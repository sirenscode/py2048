from tkinter import *
import random
from tkinter.font import Font
from functools import partial
import time
from copy import deepcopy

class game_2048(Tk):
	def __init__(self):
		super().__init__()
		self.title('2048')
		self.geometry('450x550')
		self.config(bg='white')

		self.untouch = [(i, j) for i in range(4) for j in range(4)]
		self.has_undo = False
		self.color_hex = ['#050f2c', '#003666', '#00aeff', '#3369e7', '#8e43e7', '#b84592', '#ff4f81', '#', '#', '#2dde98', '#']
		self.color = {2**i:self.color_hex[i-1] for i in range(1, len(self.color_hex)+1)}
		self.num_grid = [[0 for j in range(4)] for i in range(4)]
		self.random_start = random.choice(self.untouch)
		self.num_grid[self.random_start[0]][self.random_start[1]] = random.choice([2, 4])
		self.grid = [[Label(self, text=self.num_grid[i][j] if self.num_grid[i][j] else '', bg=self.color[self.num_grid[i][j]] if self.num_grid[i][j] else 'grey88', fg='white', justify=CENTER, font=Font(family='Clear Sans Medium', size=28)) for j in range(4)] for i in range(4)]
		self.last_numgrid = []

		self.untouch.remove(self.random_start)
		self.title = Label(self, text='2048', bg='#ffc168', font=Font(family='Clear Sans Medium', size=28), fg='white')
		self.undo_btn = Button(self, text='Undo', relief=FLAT, font=Font(family='Clear Sans Medium', size=20), bg='#ff6c5f', fg='white', command=self.undo)
		self.restart_btn = Button(self, text='New', relief=FLAT, font=Font(family='Clear Sans Medium', size=20), bg='#ff6c5f', fg='white', command=self.new_game)

		self.setup()

	def setup(self):
		for i in range(4):
			for j in range(4):
				self.grid[i][j].place(y=i*100+130, x=j*100+30, width=90, height=90)

		for i in 'wasd':
			temp_func = partial(self.move, i)
			self.bind(f'<{i}>', temp_func)

		self.title.place(x=30, y=30, width=190, height=90)
		self.undo_btn.place(x=330, y=30, width=90, height=90)
		self.restart_btn.place(x=230, y=30, width=90, height=90)

	def move(self, k, e):
		self.last_numgrid2 = self.num_grid[:]
		
		t = list(zip(*self.num_grid)) if k in 'ws' else self.num_grid[:]
		for i in range(4):
			c = dict(enumerate([j for j in (t[i]) if j][::1 if k in 'wa' else -1]))
			for j in range(len(c), 4): c[j] = 0
			for j in range(3):
				if c[j] == c[j+1]:
					c[j] = c[j]*2
					c[j+1] = 0
			c = [j for j in c.values() if j]
			c = (c+[0]*(4-len(c))) if k in 'wa' else ([0]*(4-len(c))+c[::-1])
			t[i] = c
		if k in 'ws': t = [list(i) for i in zip(*t)]
		if self.num_grid!=t: self.last_numgrid = self.num_grid[:]
		self.num_grid = t
		[[self.grid[i][j].config(text=self.num_grid[i][j] if self.num_grid[i][j] else '', bg=self.color[self.num_grid[i][j]] if self.num_grid[i][j] else 'grey88') for j in range(4)] for i in range(4)]
		self.untouch = [(i, j) for i in range(4) for j in range(4) if not self.num_grid[i][j]]
		self.update()
		time.sleep(0.1)
		if self.last_numgrid2 != self.num_grid:
			new = self.last_num_place if self.has_undo and self.last_num_place in self.untouch else random.choice(self.untouch)
			new_num = random.choice([2, 4]) if not self.has_undo else self.last_num
			self.last_num = new_num
			self.last_num_place = new[:]
			self.untouch.remove(new)
			self.num_grid[new[0]][new[1]] = new_num
			self.grid[new[0]][new[1]].config(text=new_num, bg=self.color[new_num])
			self.has_undo = False

	def undo(self):
		if hasattr(self, 'last_numgrid') and self.last_numgrid:
			self.num_grid = self.last_numgrid
			[[self.grid[i][j].config(text=self.num_grid[i][j] if self.num_grid[i][j] else '', bg=self.color[self.num_grid[i][j]] if self.num_grid[i][j] else 'grey88') for j in range(4)] for i in range(4)]
			self.untouch = [(i, j) for i in range(4) for j in range(4) if not self.num_grid[i][j]]
			self.has_undo = True

	def new_game(self):
		self.untouch = [(i, j) for i in range(4) for j in range(4)]
		self.has_undo = False
		self.num_grid = [[0 for j in range(4)] for i in range(4)]
		self.random_start = random.choice(self.untouch)
		self.num_grid[self.random_start[0]][self.random_start[1]] = random.choice([2, 4])
		self.last_numgrid = []
		self.untouch.remove(self.random_start)
		[[self.grid[i][j].config(text=self.num_grid[i][j] if self.num_grid[i][j] else '', bg=self.color[self.num_grid[i][j]] if self.num_grid[i][j] else 'grey88') for j in range(4)] for i in range(4)]

root = game_2048()
root.mainloop()