import pygame as pg
from matrix_functions import *

class Camera:
    def __init__(self, render, position):  # Initializes the camera
        self.render = render
        self.position = np.array([*position, 1.0])  # Camera position
        self.forward = np.array([0, 0, 1, 1])  # Forward direction
        self.up = np.array([0, 1, 0, 1])  # Up direction
        self.right = np.array([1, 0, 0, 1])  # Right direction
        self.horizontal_fov = math.pi / 3  # Horizontal field of view
        self.vertical_fov = self.horizontal_fov * (render.height / render.width)  # Vertical field of view
        self.near_plane = 0.1  # Near clipping plane
        self.far_plane = 100  # Far clipping plane
        self.moving_speed = 0.1  # Speed of movement
        self.rotation_speed = 0.015  # Speed of rotation

        self.anglePitch = 0  # Pitch angle
        self.angleYaw = 0  # Yaw angle
        self.angleRoll = 0  # Roll angle

    def control(self):  # Handles camera movement based on key inputs
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed

        if key[pg.K_h]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_k]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_u]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_j]:
            self.camera_pitch(self.rotation_speed)

    def camera_yaw(self, angle):  # Rotates the camera around the Y-axis
        self.angleYaw += angle

    def camera_pitch(self, angle):  # Rotates the camera around the X-axis
        self.anglePitch += angle

    def axiiIdentity(self):  # Resets camera orientation to default axes
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):  # Updates camera orientation based on rotation angles
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)
        self.axiiIdentity()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self):  # Returns the camera transformation matrix
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()

    def translate_matrix(self):  # Returns the translation matrix based on camera position
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):  # Returns the rotation matrix based on camera orientation
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
