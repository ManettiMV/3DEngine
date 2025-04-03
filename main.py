from object_3D import *
from camera import *
from projection import *
import pygame as pg
import os
"""
Author: Erick Manetti
Created and adapted based on some github 3D projects
https://github.com/ManettiMV

WASD 'walks' through the scene, EQ goes UP and Down, UHJK rotates the scene
"""
class SoftwareRender:
    def __init__(self):
        pg.init()
        self.width, self.height = 1600, 900
        self.resolution = self.width, self.height
        self.center_width, self.center_height = self.width//2, self.height//2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.resolution)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):   # Puts the object in the screen
        self.camera = Camera(self, [0, 0, -6])
        self.projection = Projection(self)
        self.object = self.get_object_from_file("eyeball.obj")
        self.object.rotate_y(-math.pi / 4)

    def get_object_from_file(self, filename):   # Get an object from a file .obj in the resources folder
        vertex, faces = [], []
        filepath = os.path.join("3D Engine",os.path.join("resources", filename))
        with open(filepath) as f:
            for line in f:  # Iterates through the vertices/faces and get them to our program
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
    
        return Object3D(self, vertex, faces)
    
    def draw(self): # Pretty self explanatory
        self.screen.fill(pg.Color("black"))
        self.object.draw()
    
    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(round(self.clock.get_fps())))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    app = SoftwareRender()
    app.run()