import pygame
from pygame.locals import QUIT
import pygame.display
import pywavefront
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time
import os
import multiprocessing
from utils.shader_loader import load_shader


class ModelRendererProcess(multiprocessing.Process):
    def __init__(self, obj_path, window_size=(800, 600)):
        super().__init__()
        self.obj_path = obj_path
        self.window_size = window_size
        self._jaw_movement_enabled = multiprocessing.Value('b', False)
        self._head_nod_enabled = multiprocessing.Value('b', False)
        self._head_shake_enabled = multiprocessing.Value('b', False)

    def run(self):
        self.renderer = ModelRenderer(self.obj_path, self.window_size)
        # Pass the shared state to the renderer
        self.renderer.jaw_movement_enabled = self._jaw_movement_enabled
        self.renderer.head_nod_enabled = self._head_nod_enabled
        self.renderer.head_shake_enabled = self._head_shake_enabled

        self.renderer.mainloop()

    def toggle_jaw_movement(self):
        with self._jaw_movement_enabled.get_lock():
            self._jaw_movement_enabled.value = not self._jaw_movement_enabled.value

    @property
    def jaw_movement_enabled(self):
        return self._jaw_movement_enabled.value

    @jaw_movement_enabled.setter
    def jaw_movement_enabled(self, value):
        self._jaw_movement_enabled.value = value
        if value:
            self.renderer.jaw_movement_start_time = time.time()

    def toggle_head_nod(self):
        with self._head_nod_enabled.get_lock():
            self._head_nod_enabled.value = not self._head_nod_enabled.value

    def toggle_head_shake(self):
        with self._head_shake_enabled.get_lock():
            self._head_shake_enabled.value = not self._head_shake_enabled.value

    @property
    def head_nod_enabled(self):
        return self._head_nod_enabled.value

    @property
    def head_shake_enabled(self):
        return self._head_shake_enabled.value

    @head_nod_enabled.setter
    def head_nod_enabled(self, value):
        self._head_nod_enabled.value = value

    @head_shake_enabled.setter
    def head_shake_enabled(self, value):
        self._head_shake_enabled.value = value


class ModelRenderer:
    def __init__(self, obj_path, window_size=(800, 600)):
        self.obj_path = obj_path
        self.window_size = window_size
        self.scene = None

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Build the path to the vertex shader file
        self.vertex_shader_path = os.path.join(current_dir, 'shaders', 'simple.vert')

        # Build the path to the fragment shader file
        self.fragment_shader_path = os.path.join(current_dir, 'shaders', 'lighting_toneMapping.frag')

        self.jaw_y_position = 0.0

        self.jaw_opening_rate = 5.0
        self.jaw_closing_rate = 5.0
        self.jaw_distance = 0.1

        self.jaw_state = "idle"
        self.jaw_opening_start_time = None
        self.jaw_opening_end_time = None
        self.jaw_closing_start_time = None
        self.jaw_closing_end_time = None
        self.jaw_start_position = 0

        self.head_nod_enabled = None
        self.head_shake_enabled = None
        self.head_nod_angle = 0
        self.head_shake_angle = 0

        self.setup_pygame()
        self.setup_opengl()
        self.load_model()

    def setup_pygame(self):
        pygame.init()
        pygame.display.set_mode(self.window_size, pygame.DOUBLEBUF | pygame.OPENGL)

    def setup_opengl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 5))
        glLightfv(GL_LIGHT1, GL_POSITION, (-5, -5, -5))

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, self.window_size[0] / self.window_size[1], 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

        self.init_shaders()

    def init_shaders(self):
        vertex_shader_code = load_shader(self.vertex_shader_path)
        fragment_shader_code = load_shader(self.fragment_shader_path)

        vertex_shader = self.compile_shader(vertex_shader_code, GL_VERTEX_SHADER)
        fragment_shader = self.compile_shader(fragment_shader_code, GL_FRAGMENT_SHADER)

        self.shader_program = glCreateProgram()
        glAttachShader(self.shader_program, vertex_shader)
        glAttachShader(self.shader_program, fragment_shader)
        glLinkProgram(self.shader_program)
        glUseProgram(self.shader_program)

    def compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        status = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if not status:
            log = glGetShaderInfoLog(shader)
            shader_type_str = 'vertex' if shader_type == GL_VERTEX_SHADER else 'fragment'
            raise RuntimeError(f"Error compiling {shader_type_str} shader: {log}")

        return shader

    def load_model(self):
        self.scene = pywavefront.Wavefront(self.obj_path, create_materials=True, collect_faces=True)

    def move_jaw(self):
        """Move the jaw up and down smoothly."""
        current_time = time.time()

        if self.jaw_movement_enabled.value and self.jaw_state == "idle":
            # Start a new opening animation
            self.jaw_state = "opening"
            self.jaw_opening_start_time = current_time
            self.jaw_opening_end_time = current_time + (1 / self.jaw_opening_rate)
            self.jaw_start_position = self.jaw_y_position
        elif not self.jaw_movement_enabled.value and self.jaw_state != "closing":
            # Start a new closing animation
            self.jaw_state = "closing"
            self.jaw_closing_start_time = current_time
            self.jaw_closing_end_time = current_time + (1 / self.jaw_closing_rate)
            self.jaw_start_position = self.jaw_y_position

        if self.jaw_state == "opening":
            elapsed_time = current_time - self.jaw_opening_start_time
            total_time = self.jaw_opening_end_time - self.jaw_opening_start_time
            t = min(1, elapsed_time / total_time)  # t goes from 0 to 1

            # Interpolate between the start position and the target open position
            target_position = -self.jaw_distance
            self.jaw_y_position = (1 - t) * self.jaw_start_position + t * target_position

            if t == 1:  # The jaw has fully opened
                if self.jaw_movement_enabled.value:
                    # Start a new closing animation
                    self.jaw_state = "closing"
                    self.jaw_closing_start_time = current_time
                    self.jaw_closing_end_time = current_time + (1 / self.jaw_closing_rate)
                    self.jaw_start_position = self.jaw_y_position
                else:
                    self.jaw_state = "idle"  # Stop the opening animation
        elif self.jaw_state == "closing":
            elapsed_time = current_time - self.jaw_closing_start_time
            total_time = self.jaw_closing_end_time - self.jaw_closing_start_time
            t = min(1, elapsed_time / total_time)  # t goes from 0 to 1

            # Interpolate between the start position and the close position
            target_position = 0
            self.jaw_y_position = (1 - t) * self.jaw_start_position + t * target_position

            if t == 1:  # The jaw has fully closed
                if self.jaw_movement_enabled.value:
                    # Start a new opening animation
                    self.jaw_state = "opening"
                    self.jaw_opening_start_time = current_time
                    self.jaw_opening_end_time = current_time + (1 / self.jaw_opening_rate)
                    self.jaw_start_position = self.jaw_y_position
                else:
                    self.jaw_state = "idle"  # Stop the closing animation

        return self.jaw_y_position

    def update_head_actions(self):
        if self.head_nod_enabled.value:
            self.head_nod_angle = (self.head_nod_angle + 1) % 360

        if self.head_shake_enabled.value:
            self.head_shake_angle = (self.head_shake_angle + 1) % 360

    def draw_model(self):
        rotation_speed = 6  # Increase this value to make the model rotate faster
        angle = (
                        time.time() * rotation_speed) % 360  # Calculate the rotation angle based on the current time and rotation speed

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 3.5, 0, 0, 0, 0, 1, 0)  # Adjust the z-value from 10 to 8 to zoom in

        glRotatef(self.head_nod_angle, 1, 0, 0)  # Rotate the model around the X-axis
        glRotatef(self.head_shake_angle, 0, 1, 0)  # Rotate the model around the Y-axis

        for name, mesh in self.scene.meshes.items():
            material = self.scene.materials['Material']
            glMaterialfv(GL_FRONT, GL_AMBIENT, material.ambient)
            glMaterialfv(GL_FRONT, GL_DIFFUSE, material.diffuse)
            glMaterialfv(GL_FRONT, GL_SPECULAR, material.specular)
            clamped_shininess = min(128, material.shininess)
            glMaterialf(GL_FRONT, GL_SHININESS, clamped_shininess)

            # Apply transformation if the name is "Cube.001"
            if name == 'Cube.001':
                glPushMatrix()  # Push the current matrix to the stack
                glTranslate(0.0, self.move_jaw(), 0.0)  # Move the object up and down

            glBegin(GL_TRIANGLES)

            for face in mesh.faces:
                face_vertices = [self.scene.vertices[vertex_i] for vertex_i in face]
                normal = self.calculate_face_normal(face_vertices)

                for vertex_i in face:
                    glColor3f(*material.diffuse[:3])
                    glNormal3f(*normal)
                    glVertex3f(*self.scene.vertices[vertex_i])

            glEnd()

            if name == 'Cube.001':
                glPopMatrix()  # Pop the old matrix from the stack to undo the transformation for the next object

    def calculate_face_normal(self, vertices):
        v1 = np.array(vertices[0])
        v2 = np.array(vertices[1])
        v3 = np.array(vertices[2])

        vec1 = v2 - v1
        vec2 = v3 - v1

        normal = np.cross(vec1, vec2)
        normal = normal / np.linalg.norm(normal)

        return normal

    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glLoadIdentity()
            gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

            self.update_head_actions()

            self.draw_model()

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Build the path to the model file
    model_path = os.path.join(current_dir, '..', 'models', 'face.obj')

    skull_renderer_process = ModelRendererProcess(model_path)
    # skull_renderer_process = ModelRendererProcess("models/face.obj")
    skull_renderer_process.start()  # Start the process
    skull_renderer_process.toggle_jaw_movement()  # Control the jaw movement
    print("Jaw movement:", skull_renderer_process.jaw_movement_enabled)
    time.sleep(7)  # Wait for 5 seconds
    skull_renderer_process.toggle_jaw_movement()  # Control the jaw movement
    print("Jaw movement:", skull_renderer_process.jaw_movement_enabled)
    time.sleep(3)  # Wait for 5 seconds
    skull_renderer_process.toggle_head_nod()  # Control the head nod
    print("Head nod:", skull_renderer_process.head_nod_enabled)
    time.sleep(5)  # Wait for 5 seconds
    skull_renderer_process.toggle_jaw_movement()  # Control the jaw movement
    print("Jaw movement:", skull_renderer_process.jaw_movement_enabled)
    time.sleep(9)  # Wait for 5 seconds
    skull_renderer_process.toggle_head_shake()  # Control the head shake
    print("Head shake:", skull_renderer_process.head_shake_enabled)
    time.sleep(5)  # Wait for 5 seconds
    skull_renderer_process.toggle_jaw_movement()  # Control the jaw movement
    print("Jaw movement:", skull_renderer_process.jaw_movement_enabled)
    time.sleep(2)  # Wait for 5 seconds
    skull_renderer_process.toggle_jaw_movement()  # Control the jaw movement
    print("Jaw movement:", skull_renderer_process.jaw_movement_enabled)
