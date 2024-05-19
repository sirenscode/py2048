from tkinter import *
import random
import sys

class Grid:
    def __init__(self, n):
        self.size = n
        self.cells = self.generate_empty_grid()
        self.compressed = False
        self.merged = False
        self.moved = False
        self.current_score = 0
        
    def generate_empty_grid(self):
        return [[0]* self.size for i in range(self.size)]
    
    def random_cell(self):
        cell = random.choice(self.retrieve_empty_cells())
        i = cell[0]
        j = cell[1]
        self.cells[i][j] = 2 if random.random() < 0.9 else 4
        
        
    def retrieve_empty_cells(self):
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    empty_cells.append((i,j))
        return empty_cells
    
    def transpose(self):
        self.cells = [list(t) for t in zip(*self.cells)]
        
    def reverse(self):
        for i in range(self.size):
            start = 0
            end = self.size - 1
            while start < end:
                self.cells[i][start], self.cells[i][end] = \
                    self.cells[i][end],self.cells[i][start]
                start += 1
                end -= 1
    
    def clear_flags(self):
        self.compressed = False
        self.merged = False
        self.moved = False
        
    def left_compress(self):
        self.compressed = False
        new_grid = self.generate_empty_grid()
        for i in range(self.size):
            count = 0
            for j in range(self.size):
                if self.cells[i][j] != 0:
                    new_grid[i][count] = self.cells[i][j]
                    if count != j:
                        self.compressed = True
                    count += 1
        self.cells = new_grid
        
    def left_merge(self):
        self.merged = False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.cells[i][j] == self.cells[i][j + 1] and \
                    self.cells[i][j] != 0:
                        self.cells[i][j] *= 2
                        self.cells[i][j+1] = 0
                        self.current_score += self.cells[i][j]
                        self.merged = True
                        
    def found_2048(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] >= 2048:
                    return True
        return False
    
    def has_empty_cells(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    return True
        return False
    
    def can_merge(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == self.cells[i][j + 1]:
                    return True
        for j in range(self.size):
            for i in range(self.size):
                if self.cells[i][j] == self.cells[i+1][j]:
                    return True
        return False
    
    def set_cells(self, cells):
        self.cells = cells
        
    def print_grid(self):
        print('-' * 40)
        for i in range(self.size):
            for j in range(self.size):
                print('%d\t' % self.cells[i][j], end='')
            print()
        print('-' * 40)
        
class GamePanel:
    BACKGROUND_COLOR = '#eee'
    EMPTY_CELL_COLOR = '#e0e0e0'
    CELL_BACKGROUND_COLOR_DICT = {
        '2': '#050f2c',
        '4': '#003666',
        '8': '#00aeff',
        '16': '#3369e7',
        '32': '#8e43e7',
        '64': '#b84592',
        '128': '#ff4f81',
        '256': '#edcc61',
        '512': '#ffc168',
        '1024': '#ff6c5f',
        '2048': '#b84592',
        'beyond': '#3c3a32'
    }
    CELL_COLOR_DICT = {
        '2': '#ffffff',
        '4': '#ffffff',
        '8': '#ffffff',
        '16': '#ffffff',
        '32': '#ffffff',
        '64': '#ffffff',
        '128': '#ffffff',
        '256': '#ffffff',
        '512': '#ffffff',
        '1024': '#ffffff',
        '2048': '#ffffff',
        'beyond': '#ffffff'
    }
        
    FONT = ('Clear Sans Medium', 28)
    UP_KEYS = ('w', 'W', 'Up')
    LEFT_KEYS = ('a', 'A', 'Left')
    DOWN_KEYS = ('s', 'S', 'Down')
    RIGHT_KEYS = ('d', 'D', 'Right')
        
    def __init__(self,grid):
        self.grid = grid
        self.root = Tk()
        self.root.title("2048")
        self.root.resizable(False,False)
        self.background = Frame(self.root, bg=GamePanel.BACKGROUND_COLOR)
        self.cell_labels = []
        for i in range(self.grid.size):
            row_labels = []
            for j in range(self.grid.size):
                label = Label(self.background,text='',
                              bg=GamePanel.EMPTY_CELL_COLOR,
                              justify=CENTER,
                              font=GamePanel.FONT,
                              width=4,height=2)
                label.grid(row=i,column=j,padx=5,pady=5)
                row_labels.append(label)
            self.cell_labels.append(row_labels)
        self.background.pack(side=TOP)
        
    def paint(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                if self.grid.cells[i][j] == 0:
                    self.cell_labels[i][j].configure(
                        text="",
                        bg=GamePanel.EMPTY_CELL_COLOR
                    )
                else:
                    cell_text = str(self.grid.cells[i][j])
                    if self.grid.cells[i][j] > 2048:
                        bg_color = GamePanel.CELL_BACKGROUND_COLOR_DICT.get("beyond")
                        fg_color = GamePanel.CELL_COLOR_DICT.get('beyond')
                    else:
                        bg_color = GamePanel.CELL_BACKGROUND_COLOR_DICT.get(cell_text)
                        fg_color = GamePanel.CELL_COLOR_DICT.get(cell_text)
                    self.cell_labels[i][j].configure(
                        text=cell_text,
                        bg=bg_color,fg=fg_color)
                    

class Game:
    def __init__(self,grid, panel):
        self.grid = grid
        self.panel = panel
        self.start_cells_num = 2
        self.panel = panel
        self.over = False
        self.won = False
        self.keep_playing = False
        
    def is_game_terminated(self):
        return self.over or (self.won and (not self.keep_playing))
        
    def start(self):
        self.add_start_cells()
        self.panel.paint()
        self.panel.root.bind('<Key>',self.key_handler)
        self.panel.root.mainloop()
        
    def add_start_cells(self):
        for i in range(self.start_cells_num):
            self.grid.random_cell()
            
    def can_move(self):
        return self.grid.has_empty_cells() or self.grid.can_merge()
    
    def key_handler(self,event):
        if self.is_game_terminated():
            return
        
        self.grid.clear_flags()
        key_value = event.keysym
        print(f"{key_value} key pressed")
        if key_value in GamePanel.UP_KEYS:
            self.up()
        elif key_value in GamePanel.DOWN_KEYS:
            self.down()
        elif key_value in GamePanel.RIGHT_KEYS:
            self.right()
        elif key_value in GamePanel.LEFT_KEYS:
            self.left()
        else:
            pass
        
        self.panel.paint()
        print(f"SCORE: {self.grid.current_score}")
        if self.grid.found_2048:
            self.you_win()
            if not self.keep_playing:
                return
            
        if self.grid.moved:
            self.grid.random_cell()
            
        self.panel.paint()
        if not self.can_move():
            self.over = True
            self.game_over()
            
    def you_win(self):
        if not self.won:
            self.won = True
            print("YOU WIN")
            self.keep_playing = True
            
    def game_over(self):
        print("GAME OVER")
        
    def up(self):
        self.grid.transpose()
        self.grid.left_compress()
        self.grid.left_merge()
        self.grid.moved = self.grid.compressed or self.grid.merged
        self.grid.left_compress()
        self.grid.transpose()

    def left(self):
        self.grid.left_compress()
        self.grid.left_merge()
        self.grid.moved = self.grid.compressed or self.grid.merged
        self.grid.left_compress()
        
    def down(self):
        self.grid.transpose()
        self.grid.reverse()
        self.grid.left_compress()
        self.grid.left_merge()
        self.grid.moved = self.grid.compressed or self.grid.merged
        self.grid.left_compress()
        self.grid.reverse()
        self.grid.transpose()

    def right(self):
        self.grid.reverse()
        self.grid.left_compress()
        self.grid.left_merge()
        self.grid.moved = self.grid.compressed or self.grid.merged
        self.grid.left_compress()
        self.grid.reverse()
        
if __name__ == '__main__':
    size = 4
    grid = Grid(size)
    panel = GamePanel(grid)
    main_game = Game(grid,panel)
    main_game.start()
        
        
                    
                        