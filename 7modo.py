import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image

# Definir el código del shader
vertex_shader = """
#version 330
layout(location = 0) in vec2 position;
layout(location = 1) in vec2 tex_coords;

out vec2 frag_tex_coords;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    frag_tex_coords = tex_coords;
}
"""

fragment_shader = """
#version 330
in vec2 frag_tex_coords;
out vec4 fragColor;

uniform sampler2D texture_sampler;

void main()
{
    fragColor = texture(texture_sampler, frag_tex_coords);
}
"""

# Dimensiones de la ventana
window_width = 800
window_height = 600

# Textura de ejemplo
texture_path = "texture.png"

# Función para cargar una textura desde un archivo de imagen
def load_texture(file_path):
    try:
        image = Image.open(file_path)
        image_data = image.tobytes("raw", "RGBA", 0, -1)
        
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        
        return texture_id
    
    except Exception as e:
        print("Error loading texture:", str(e))
        return 0

# Función para inicializar OpenGL y cargar la textura
def initialize():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    
    global texture_id
    texture_id = load_texture(texture_path)
    
    # Compilar el shader
    vertex_shader_id = compileShader(vertex_shader, GL_VERTEX_SHADER)
    fragment_shader_id = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    global shader_program
    shader_program = compileProgram(vertex_shader_id, fragment_shader_id)

# Función para dibujar la escena
def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Configurar proyección ortográfica
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    
    # Configurar matriz de vista
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Dibujar un cuadrado con la textura
    glUseProgram(shader_program)
    
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(window_width, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(window_width, window_height)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(0, window_height)
    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, 0)
    glUseProgram(0)
    
    glFlush()

# Función principal
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Texture Display")
    
    initialize()
    
    glutDisplayFunc(draw_scene)
    glutMainLoop()

if __name__ == "__main__":
    main()
