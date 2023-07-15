import sys
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image

# Definir el código del shader
vertex_shader = """
#version 330
layout(location = 0) in vec2 position;

uniform mat4 projection;
uniform mat4 modelview;

out vec2 tex_coords;

void main()
{
    gl_Position = projection * modelview * vec4(position, 0.0, 1.0);
    tex_coords = position;
}
"""

fragment_shader = """
#version 330
in vec2 tex_coords;
out vec4 fragColor;

uniform sampler2D texture_sampler;

void main()
{
    fragColor = texture(texture_sampler, tex_coords);
}
"""

# Parámetros del modo 7
scale_x = 1.5
scale_y = 1.5
rotation_angle = 30

# Textura de ejemplo
texture_image_path = "texture.png"

# Función para cargar una textura desde un archivo de imagen
def load_texture(file_path):
    try:
        image = Image.open(file_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        width, height = image.size
        image_data = image.tobytes("raw", "RGBA", 0, -1)
        
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        
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
    texture_id = load_texture(texture_image_path)
    print("Texture loaded successfully")
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
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
    
    # Configurar matriz de vista
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Aplicar transformaciones del modo 7
    glScalef(scale_x, scale_y, 1.0)
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)
    
    # Dibujar un cuadrado con la textura
    glUseProgram(shader_program)
    
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(-1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(-1.0, 1.0)
    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, 0)
    glUseProgram(0)
    
    glFlush()

# Función para actualizar la posición de la cámara
def update_camera_position():
    global rotation_angle
    rotation_angle += 0.5

# Función para manejar el evento de renderizado
def render():
    update_camera_position()
    draw_scene()
    glutSwapBuffers()

# Función principal
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1920*2, 1080*2)
    glutCreateWindow(b"Mode 7 Effect")
    
    initialize()
    
    glutDisplayFunc(render)
    glutIdleFunc(render)
    
    glutMainLoop()

if __name__ == "__main__":
    main()

