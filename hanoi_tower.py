#!/usr/bin/env python3
# Piotr Beling, 2024

import pyglet
from pyglet import shapes, clock
from pyglet.window import key

class HanoiWondow(pyglet.window.Window):
    
    def __init__(self):
        super().__init__(caption="Tower of Hanoi", resizable=True)
        self.reset_game(4)

    def reset_game(self, max_disk):
        self.max_disk = max_disk
        self.position = [d for d in range(self.max_disk, -1, -1)], [], []
        self.plan = [(self.max_disk, 0, 1)]
        self.auto_play_time = None
        clock.schedule(self.auto_play)
        self.selected_rod = None

    def auto_play(self, dt):
        '''Play optimal move each 1 second or do nothing if auto_play_time is None'''
        if self.auto_play_time is None: return
        self.auto_play_time += dt
        if self.auto_play_time > 1:
            self.auto_play_time = 0
            self.make_optimal_move()
        
    def make_move(self, src, dst):
        '''Move one disk from src to dst.'''
        self.position[dst].append(self.position[src].pop())
        
    def push_to_plan(self, src, dst):
        '''Plan moving one disk from src to dst.'''
        self.plan.append((0, src, dst))
        
    def make_user_move(self, src, dst):
        '''Move one disk from src to dst and plan corrective moves.'''
        optimal_move = self.optimal_move()  # optimal move
        if optimal_move is None:    # if the game is already solved
            self.push_to_plan(dst, src) # unmaking the move solves it again
        else:
            optim_src, optim_dst = optimal_move
            if src == optim_src:    # disk to play is right
                if dst != optim_dst:    # but the destination is wong
                    self.push_to_plan(dst, optim_dst) # move from wrong to right destination to fix
            else:   # disk to play is wrong, to fix:
                self.push_to_plan(optim_src, optim_dst) # make correct move
                self.push_to_plan(dst, src) # after unmake the wrong one
        self.make_move(src, dst)
        
    def select(self, rod):
        '''Try to select the rod or try to make a move if another rod is already selected.'''
        if self.selected_rod is None:
            if self.position[rod]:
                self.selected_rod = rod
        else:
            if self.selected_rod == rod:
                self.selected_rod = None
                return
            d = self.position[self.selected_rod][-1]
            if not self.position[rod] or self.position[rod][-1] > d:
                self.make_user_move(self.selected_rod, rod)
                self.selected_rod = None
        
    def make_optimal_move(self):
        '''Make optimal move is the game is not already solved.'''
        try:
            src, dst = self.optimal_move()
        except TypeError:
            pass
        else:
            self.make_move(src, dst)
        
    def optimal_move(self):
        '''Get optimal move or None if the game is already solved.'''
        if not self.plan: return None
        n, src, dst = self.plan.pop()
        while n > 0:
            third = 3 - src - dst
            n -= 1
            self.plan.append((n, third, dst))
            self.plan.append((0, src, dst))
            dst = third
        return src, dst
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key._1: self.select(0)
        if symbol == key._2: self.select(1)
        if symbol == key._3: self.select(2)
        if symbol in (key.ENTER, key.NUM_ENTER, key.SPACE): self.make_optimal_move()
        if symbol in (key.PLUS, key.NUM_ADD) and self.max_disk < 8: self.reset_game(self.max_disk+1)
        if symbol in (key.MINUS, key.NUM_SUBTRACT) and self.max_disk > 1: self.reset_game(self.max_disk-1)
        if symbol == key.P: self.auto_play_time = 0 if self.auto_play_time is None else None
        
    def on_mouse_press(self, x, y, button, modifiers):
        if y > self.height-60:
            self.make_optimal_move()
        else:
            self.select(x * 3 // self.width)

    def on_draw(self):
        rod_x_center = self.width / 4
        rod_width = self.width / 5
        rod_y = self.height / 5
        rod_height = 3 * self.height / 5
        disk_height = rod_height/10
        min_disk_width = rod_width / 2 
        disk_width_delta = rod_width * 9 / 10 - min_disk_width 
        
        self.clear()
        for rod_i in range(3):
            rod_x = rod_x_center*(rod_i+1)
            rod_color = color=(123, 123, 255) if rod_i == self.selected_rod else (55, 55, 255)
            base = shapes.Rectangle(
                rod_x, rod_y,
                rod_width, disk_height,
                rod_color)
            base.anchor_position = rod_width/2, disk_height
            base.draw()
            rod = shapes.Rectangle(
                rod_x, rod_y,
                rod_width/10, rod_height,
                rod_color)
            rod.anchor_x = rod_width/20
            rod.draw()
            for d_i, d in enumerate(self.position[rod_i]):
                disk_w = min_disk_width + disk_width_delta * d / self.max_disk
                disk = shapes.Rectangle(rod_x, rod_y+d_i*disk_height+d_i+1,
                                       disk_w, disk_height,
                                       (255 * d // self.max_disk,
                                       255 * (self.max_disk-d) // self.max_disk,
                                       0))
                disk.anchor_x = disk_w/2
                disk.draw()
        pyglet.text.Label('Make optimal move (ENTER)',
                          font_size=36,
                          x=window.width//2, y=self.height-30,
                          anchor_x='center', anchor_y='center').draw()

window = HanoiWondow()
pyglet.app.run()
