import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

glfw.init()

glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(720, 600, "Minha primeira janela", None, None)

glfw.make_context_current(window)

def key_event(window, key, scancode, action, mods):
    print('[key event] key=',key)
    print('[key event] scancode=',scancode)
    print('[key event] action=',action)
    print('[key event] mods=',mods)
    print("-----")

glfw.set_key_callback(window, key_event)

def mouse_event(window, button, action, mods):
    print('[mouse event] button=',button)
    print('[mouse event] action=',action)
    print('[mouse event] mods=',mods)
    print("-----")

glfw.set_mouse_button_callback(window, mouse_event)

glfw.show_window(window)

R = 0.2
G = 1.0
B = 0.5
while not glfw.window_should_close(window):

    
    # funcao interna do glfw para gerenciar eventos de mouse, teclado, etc
    glfw.poll_events() 

    # limpa a cor de fundo da janela e preenche com outra no sistema RGBA
    glClear(GL_COLOR_BUFFER_BIT)
    
    # definindo a cor da janela      
    glClearColor(R, G, B, 1.0)

    # gerencia troca de dados entre janela e o OpenGL
    glfw.swap_buffers(window)
