#!/usr/bin/python2

# John Conway's Game of Life on toroidal topology.

# Antonio Garro, 2014.
# This code is in the public domain.

import pygtk
pygtk.require('2.0')
import gtk

class GUI():
    def __init__(self, seed=(75,50), speed=500):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_resizable(False)
        window.set_title("Conway's Game of Life")
        window.connect("destroy", lambda w: gtk.main_quit())
        
        self.scale = 10
        self.speed = speed
        if type(seed) == tuple and len(seed) == 2:
            size = (self.scale*seed[0], self.scale*seed[1])
        else:
            size = (self.scale*75, self.scale*50)
        
        self.bg = 0
        self.bg_colors = [gtk.gdk.color_parse('light grey'),
                          gtk.gdk.color_parse('white')]
        
        self.area = gtk.DrawingArea()
        self.area.set_size_request(size[0], size[1])
        self.area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.area.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.area.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.area.set_flags(gtk.CAN_FOCUS)
        self.area.grab_focus()

        self.area.connect("button-press-event", self.press_cb)
        self.area.connect("expose-event", self.area_expose_cb)
        self.area.connect("motion-notify-event", self.move_cb)
        self.area.connect("key-press-event", self.key_cb)
        self.area.modify_bg(gtk.STATE_NORMAL, self.bg_colors[self.bg])
        self.area.show()
        
        window.add(self.area)
        window.show()
        self.alive = 0
        self.world = World(seed)
        print("Ctrl+Move to draw.\nCtrl+Shift+Move to erase.\nRight click to switch on/off.\nLeft click to toggle cell.")
    
    def press_cb(self, widget, event):
        if event.button == 3:
            x, y = int(event.x/self.scale), int(event.y/self.scale)
            self.world.cells[y][x] = not self.world.cells[y][x]
            self.area.queue_draw()
        else:
            self.alive = not self.alive
            self.toggle_background()
            gtk.timeout_add(self.speed, self.iterate)
        return True
    
    def move_cb(self, widget, event):
        if not self.alive and event.state & gtk.gdk.CONTROL_MASK:
            x, y = int(event.x/self.scale), int(event.y/self.scale)
            self.world.cells[y][x] = not event.state & gtk.gdk.SHIFT_MASK
            self.area.queue_draw()
        return True

    def key_cb(self, widget, event):
        if(gtk.gdk.keyval_name(event.keyval) == "Escape"):
            gtk.main_quit()
        return True
        
    def iterate(self, a=None,b=None):
        if self.alive:
            self.world.iterate()
            self.area.queue_draw()
            return True
        else:
            return False

    def toggle_background(self):
        self.bg = 1- self.bg
        self.area.modify_bg(gtk.STATE_NORMAL, self.bg_colors[self.bg])
        
    def area_expose_cb(self, area, event):
        self.draw(self.world.cells)
        return True
        
    def draw_point(self, x, y):
        self.style = self.area.get_style()
        self.area.window.draw_rectangle(self.style.black_gc, True, x, y, self.scale, self.scale)
            
    def draw(self, data):
        for y,Y in enumerate(data):
            for x,X in enumerate(Y):
                if X:
                    self.draw_point(self.scale*x, self.scale*y)


class World():
    def __init__(self, seed = 0):
        if type(seed) == tuple and len(seed) == 2:
            self.size = seed
        else:
            self.size = (70,50)
            
        self.cells = [[0 for x in range(self.size[0])] for y in range(self.size[1])]
            
    def cell_status(self, x, y):
        n = self.sum_neighbours(x, y)
        if n < 3:
            return 0
        elif n == 3:
            return 1
        elif n == 4:
            return self.cells[y][x]
        else:
            return 0
        
    def sum_neighbours(self, x, y):
        return sum(self.cells[(y+i)%self.size[1]][(x+j)%self.size[0]] for i in range(-1,2) for j in range(-1,2))

    def new_status(self):
        return [[self.cell_status(x,y) for x in range(self.size[0])] for y in range(self.size[1])]
        
    def print_world(self):  #unused.
        for v in self.cells:
            print (v)
        print()

    def iterate(self):
        self.cells = self.new_status()
        return True
        #self.print_world()
GUI()
gtk.main()
