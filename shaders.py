from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileShader, compileProgram

import numpy as np
import ctypes

# Dimensiones de la ventana de visualización
width, height = 800, 600

# Código GLSL
vertex_shader = """
#version 330
void main() {
    gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330
out vec4 fragColor;

uniform vec2 iResolution;
uniform float iTime;

// Resto del código GLSL ...

const float PI   =   3.141592;

const float pot  =  1.1;
const float freq = 222.1;

vec3 paletteReal( float t ) {
    
    float w = 380. + 400.*(1.-t);
    float red, green, blue;

    if (w >= 380. && w < 440.) {
        red   = -(w - 440.) / (440. - 380.);
        green = 0.;
        blue  = 1.;
    }
    else 
    if (w >= 440. && w < 490.) {
        red   = 0.;
        green = (w - 440.) / (490. - 440.);
        blue  = 1.;
    }
    else 
    if (w >= 490. && w < 510.) {
        red   = 0.;
        green = 1.;
        blue  = -(w - 510.) / (510. - 490.);
    }
    else 
    if (w >= 510. && w < 580.) {
        red   = (w - 510.) / (580. - 510.);
        green = 1.;
        blue  = 0.;
    }
    else 
    if (w >= 580. && w < 645.) {
        red   = 1.;
        green = -(w - 645.) / (645. - 580.);
        blue  = 0.;
    }
    else 
    if (w >= 645. && w < 781.) {
        red   = 1.;
        green = 0.;
        blue  = 0.;
    }
    else {
        red   = 0.;
        green = 0.;
        blue  = 0.;
    }


    // Let the intensity fall off near the vision limits
    float factor;
    if (w >= 380. && w < 420.)
        factor = .3 + .7*(w - 380.) / (420. - 380.);
    else 
    if (w >= 420. && w < 701.)
        factor = 1.;
    else 
    if (w >= 701. && w < 781.)
        factor = .3 + .7*(780. - w) / (780. - 700.);
    else
        factor = 0.;

    float gamma = .8;
    float R = (red   > 0. ? 255.*pow(red   * factor, gamma) : 0.);
    float G = (green > 0. ? 255.*pow(green * factor, gamma) : 0.);
    float B = (blue  > 0. ? 255.*pow(blue  * factor, gamma) : 0.); 
    
    return vec3(R/255.,G/255.,B/255.);
    //return vec3(r,0.,b);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    float yRat = (iResolution.y/iResolution.x);
    
    vec2 uv = 2.*(fragCoord/iResolution.x - vec2(.5,yRat/2.));
    
    float x = uv.x;
    float y = uv.y;

    
    float valxy = 
         1.- 
         (1.+sin(freq*(x)*pow(iTime,pot) ))/2.
         * 
         (1.+cos(freq*(y)*pow(iTime,pot) ))/2.
         ;
    
    
    
    //plot (1-(1-sin( 10*(x+y) * x)^100) * 
    //        (1-sin( 10*(x+y) * y)^100))    
    
    //float valxy = 
    //    //1. -
    //     pow( (1.+sin((2.*PI)*freq*iTime*(x*y-y)))/2., pot) * 
    //     pow( (1.+cos((2.*PI)*freq*iTime*(y*x-x)))/2., pot);
    
    
    //float valxy = 
    //      1. -
    //     pow( (1.+sin((2.*PI)*freq*iTime*(x/y)))/2., pot) * 
    //     pow( (1.+cos((2.*PI)*freq*iTime*(y/x)))/2., pot);
    
    
    //float valxy = 
    //     //1. -
    //     (1.+cos(freq*x*iTime))/2. 
    //     * 
    //     (1.+cos(freq*y*iTime))/2. 
    //     ;
    
    //vec3 col = vec3(valxy);
    vec3 col = paletteReal(valxy);
    
    
    // Output to screen
    fragColor = vec4(col,1.0);
}

void main() {
    vec2 fragCoord = gl_FragCoord.xy;
    mainImage(fragColor, fragCoord);
}
"""

def display():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)

    # Establecer valores de iResolution e iTime
    iResolution_location = glGetUniformLocation(shader_program, "iResolution")
    glUniform2f(iResolution_location, width, height)
    iTime_location = glGetUniformLocation(shader_program, "iTime")
    glUniform1f(iTime_location, glutGet(GLUT_ELAPSED_TIME) / 1000.0)

    glDrawArrays(GL_TRIANGLES, 0, 3)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"GLSL Execution")

    vertex_shader_id = compileShader(vertex_shader, GL_VERTEX_SHADER)
    fragment_shader_id = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

    global shader_program
    shader_program = compileProgram(vertex_shader_id, fragment_shader_id)

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMainLoop()

if __name__ == '__main__':
    main()

