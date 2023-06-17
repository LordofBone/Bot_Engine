from OpenGL.GL import *


class ShaderEngine:
    def __init__(self, vertex_shader_path, fragment_shader_path):
        """
        Initialize the ShaderEngine with the paths of the vertex shader and fragment shader.
        """
        self.vertex_shader_code = self.load_shader(vertex_shader_path)
        self.fragment_shader_code = self.load_shader(fragment_shader_path)

    def load_shader(self, shader_file):
        """
        Load shader from file.
        """
        try:
            with open(shader_file, 'r') as f:
                shader_code = f.read()
        except FileNotFoundError:
            print(f"No such file: {shader_file}")
            return None
        return shader_code

    def compile_shader(self, source, shader_type):
        """
        Compile the shader code.
        """
        if not source:
            print("No shader source code provided for compilation.")
            return None

        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        # Check the compilation status
        status = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if not status:
            log = glGetShaderInfoLog(shader)
            shader_type_str = 'vertex' if shader_type == GL_VERTEX_SHADER else 'fragment'
            raise RuntimeError(f"Error compiling {shader_type_str} shader: {log}")

        return shader

    def create_shader_program(self, vertex_shader, fragment_shader):
        """
        Create a shader program with vertex and fragment shaders.
        """
        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)
        glUseProgram(shader_program)

        return shader_program

    def init_shaders(self):
        """
        Initialize shaders: compile the shader codes and create shader program.
        """
        vertex_shader = self.compile_shader(self.vertex_shader_code, GL_VERTEX_SHADER)
        fragment_shader = self.compile_shader(self.fragment_shader_code, GL_FRAGMENT_SHADER)

        # Check if shaders compiled successfully
        if vertex_shader is None or fragment_shader is None:
            return None

        return self.create_shader_program(vertex_shader, fragment_shader)
