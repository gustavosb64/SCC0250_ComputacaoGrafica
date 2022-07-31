import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

#Inicializando a janela
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(720, 600, "Pontos", None, None)
glfw.make_context_current(window)

#Capturando eventos de teclado
def key_event(window,key,scancode,action,mods):
    print('[key event] key=',key)
    print('[key event] scancode=',scancode)
    print('[key event] action=',action)
    print('[key event] mods=',mods)
    print('-------')

    #if key == 'ESCAPE' close window
    if key == 256:
        glfw.set_window_should_close(window, True)

glfw.set_key_callback(window,key_event)

#Capturando eventos de mouse
def mouse_event(window,button,action,mods):
    print('[mouse event] button=',button)
    print('[mouse event] action=',action)
    print('[mouse event] mods=',mods)
    print('-------')
glfw.set_mouse_button_callback(window,mouse_event)

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

"""
num_vertices = 6
#For squares and rectangles
vertices = np.zeros(4, [("position", np.float32, 2)])
vertices['position'] = [
            (0.0, 0.0),
            (0.0, 0.5),
            (0.5, 0.5),
            (0.5, 0.0),
        ] 
"""

#For circles
num_vertices = 64
vertices = np.zeros(num_vertices, [("position", np.float32, 2)])
angle = 2*math.pi/num_vertices
cur_angle = 0.0
r = 1.0

for i in range(num_vertices):
    cur_angle += angle
    x = r * math.cos(cur_angle)
    y = r * math.sin(cur_angle)
    vertices[i] = [x, y]
     

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
#    glClearColor(0.2, 1.0, 0.5, 1.0)
    glClearColor(1.0, 1.0, 1.0, 1.0)

#    glDrawArrays(GL_LINES, 0, len(vertices))
#    glDrawArrays(GL_LINE_LOOP, 0, len(vertices))
    glDrawArrays(GL_LINE_STRIP, 0, len(vertices))

#    glDrawArrays(GL_TRIANGLES, 0, len(vertices))
#    glDrawArrays(GL_TRIANGLE_STRIP, 0, len(vertices))
#    glDrawArrays(GL_TRIANGLE_FAN, 0, len(vertices))

    glfw.swap_buffers(window)

glfw.terminate()
