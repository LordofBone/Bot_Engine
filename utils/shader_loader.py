def load_shader(shader_file):
    with open(shader_file, 'r') as f:
        shader_code = f.read()
    return shader_code
