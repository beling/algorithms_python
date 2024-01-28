#!/usr/bin/env python3
# Piotr Beling, 2024

import pyglet
from pyglet import shapes, clock
from pyglet.window import key

class HanoiWondow(pyglet.window.Window):
    
    def __init__(self):
        super().__init__(resizable=True)
        self.max_disk = 4
        self.position = [d for d in range(self.max_disk, -1, -1)], [], []
        self.plan = [(self.max_disk, 0, 1)]
        #clock.schedule_interval(lambda _: self.make_step(), 1)
        self.selected_rod = None
        
    def make_move(self, a, b):
        self.position[b].append(self.position[a].pop())
        
    def push_to_plan(self, a, b):
        self.plan.append((0, a, b))
        
    def make_user_move(self, src, dst):
        step = self.step()  # optimal move
        if step is None:    # if the game is already solved
            self.push_to_plan(dst, src) # unmaking the move solves it again
        else:
            optim_src, optim_dst = step
            if src == optim_src:    # disk to play is right
                if dst != optim_dst:    # but the destination is wong
                    self.push_to_plan(dst, optim_dst) # move from wrong to right destination to fix
            else:   # disk to play is wrong, to fix:
                self.push_to_plan(optim_src, optim_dst) # make correct move
                self.push_to_plan(dst, src) # after unmake the wrong one
        self.make_move(src, dst)
        
    def select(self, rod):
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
        
    def make_step(self):
        try:
            a, b = self.step()
        except TypeError:
            pass
        else:
            self.make_move(a, b)
        
    def step(self):
        if not self.plan: return None
        n, a, b = self.plan.pop()
        while n > 0:
            c = 3 - a - b
            n -= 1
            self.plan.append((n, c, b))
            self.plan.append((0, a, b))
            b = c
        return a, b
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key._1: self.select(0)
        if symbol == key._2: self.select(1)
        if symbol == key._3: self.select(2)
        if symbol == key.ENTER or symbol == key.SPACE: self.make_step()
        
    def on_mouse_press(self, x, y, button, modifiers):
        if y > self.height-60:
            self.make_step()
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
