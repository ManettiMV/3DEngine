import pygame as pg
from matrix_functions import *
from numba import njit

@njit(fastmath=True)
def any_func(arr, a, b):  # Checks if any element in the array is equal to 'a' or 'b'
    return np.any((arr == a) | (arr == b))

class Object3D:
    def __init__(self, render, vertices='', faces=''):  # Initializes the 3D object
        self.render = render
        self.vertices = np.array(vertices)
        self.faces = faces
        self.translate([0.0001, 0.0001, 0.0001])  # Slight translation to avoid errors

        self.font = pg.font.SysFont('Arial', 30, bold=True)  
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]  # Face colors
        self.movement_flag, self.draw_vertices = True, False  
        self.label = ''  

    def draw(self): 
        self.screen_projection()
        self.movement()

    def movement(self):  # Rotates the object around the Y-axis
        if self.movement_flag:
            self.rotate_y(-(pg.time.get_ticks() % 0.005))

    def screen_projection(self):  # Projects the 3D object onto the screen
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)  # Perspective division
        vertices[(vertices > 2) | (vertices < -2)] = 0  # Clipping
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]  # Convert to 2D screen coordinates

        for index, color_face in enumerate(self.color_faces):  # Draws the object faces
            color, face = color_face
            polygon = vertices[face]
            if not any_func(polygon, self.render.center_width, self.render.center_height):
                pg.draw.polygon(self.render.screen, color, polygon, 1)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])

        if self.draw_vertices:  # Draws the vertices if enabled
            for vertex in vertices:
                if not any_func(vertex, self.render.center_width, self.render.center_height):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

    def translate(self, pos):  # Moves the object by a given position
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):  # Scales the object by a given factor
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):  # Rotates the object around the X-axis
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):  # Rotates the object around the Y-axis
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):  # Rotates the object around the Z-axis
        self.vertices = self.vertices @ rotate_z(angle)

class Axes(Object3D):
    def __init__(self, render):  # Initializes the 3D axes for reference
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])  # Axis points
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])  # Lines for the axes
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]  # Axis colors
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]  # Assign colors to faces
        self.draw_vertices = False  # Disable vertex drawing
        self.label = 'XYZ'  # Labels for the axes
