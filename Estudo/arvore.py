import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

#Inicializando a janela
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(500, 500, "Pontos", None, None)
glfw.make_context_current(window)

#Capturando eventos de teclado
def key_event(window,key,scancode,action,mods):

    #if key == 'ESCAPE' or == 'q' close window
    if key == 256 or key == 81:
        glfw.set_window_should_close(window, True)

glfw.set_key_callback(window,key_event)

#Capturando eventos de mouse
#def mouse_event(window,button,action,mods):
#glfw.set_mouse_button_callback(window,mouse_event)

#GLSL para Vertex Shader
vertex_code = """ 
            attribute vec2 position;
            void main(){
                gl_Position = vec4(position, 0.0, 1.0);
            }
            """

#GLSL para Fragment Shader
fragment_code = """ 
            void main(){
                gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
            }
            """
#Requisitando slot para a GPU para nossos programas vertex
program  = glCreateProgram()
vertex   = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

#Associando nossos códigos-fonte aos slots
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

#Compilando Vertex Shader
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")

#Compilando Fragment Shader
glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

glAttachShader(program, vertex)
glAttachShader(program, fragment)

#Linkagem do programa
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    
# Make program the default program
glUseProgram(program)

#Preparando para enviar dados para a GPU

"""
num_vertices = 4
#For lines and triangles
vertices = np.zeros(6, [("position", np.float32, 2)])
vertices['position'] = [
            (0.5, 0.5),
            (+0.9, +0.25),
            (+0.5, 0.0),
            (+0.25, -0.5),
            (-0.5, -0.25),
            (-0.25, -0.8)
        ] 
"""

num_vertices = 6

#For squares and rectangles
vertices = np.zeros(4, [("position", np.float32, 2)])
vertices['position'] = [
            (3.0, 0.0),
            (0.0, 0.0),
            (3.0, 1.0),
            (1.0, 3.0),
        ] 

"""

#For circles
num_vertices = 64
vertices = np.zeros(num_vertices*2, [("position", np.float32, 2)])
angle = 2*math.pi/num_vertices
cur_angle = 0.0
r = 0.2

for i in range(num_vertices):
    cur_angle += angle
    x = r * math.cos(cur_angle)
    y = r * math.sin(cur_angle)

    x += 0.5
    y += 0.8
    vertices[i] = [x, y]
     
"""

# Request a buffer slot from GPU
buffer = glGenBuffers(1)
# Make this buffer the default one
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Upload data
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Bind the position attribute
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)

#Associando variávies GLSL com os nossos dados
loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)

glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

glfw.show_window(window)

while not glfw.window_should_close(window):
    
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)

#    glDrawArrays(GL_LINES, 0, len(vertices))
#    glDrawArrays(GL_LINE_LOOP, 0, len(vertices))
#    glDrawArrays(GL_LINE_STRIP, 0, 6)

#    glDrawArrays(GL_TRIANGLES, 0, 6)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
#    glDrawArrays(GL_TRIANGLE_FAN, 0, 64)

    glfw.swap_buffers(window)

glfw.terminate()
