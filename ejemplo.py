import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileProgram, compileShader

# Definir el código del shader
vertex_shader = """
#version 330
layout(location = 0) in vec3 position;

void main()
{
    gl_Position = vec4(position, 1.0);
}
"""

fragment_shader = """
#version 330
out vec4 fragColor;

void main()
{
    fragColor = vec4(1.0, 1.0, 0.0, 1.0);
}
"""

# Texto de ejemplo
text = "Hello, World!"

# Función para dibujar el texto en la ventana
def draw_text():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    glUseProgram(shader_program)
    
    glRasterPos2f(-0.9, 0.9)  # Posición del texto
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))  # Renderizar cada carácter del texto

    glUseProgram(0)
    glFlush()

# Función principal
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(1920, 1080)
    glutCreateWindow(b"OpenGL Text Shader")
    
    # Compilar el shader
    vertex_shader_id = compileShader(vertex_shader, GL_VERTEX_SHADER)
    fragment_shader_id = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    global shader_program
    shader_program = compileProgram(vertex_shader_id, fragment_shader_id)
    
    glutDisplayFunc(draw_text)
    glutMainLoop()

if __name__ == "__main__":
    main()
