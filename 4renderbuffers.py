#! /usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.framebufferobjects import *
from Image import *
from OpenGL.GL.shaders import *

ESCAPE = '\033'
global angle
angle = 0.0
global size
size = 512
global shadernumber
shadernumber = 0


def drawQuad(B, T, L, R):
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(B, L,  1.0)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0)
    glVertex3f(T, L, 1.0)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0)
    glVertex3f(T,  R,  1.0)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0)
    glVertex3f(B, R, 1.0)  # Top Left Of The Texture and Quad
    glEnd()


def DrawTeapot(view, angle, buffernum):
    glBindFramebuffer(GL_FRAMEBUFFER, buffernum)
    glBindRenderbuffer(GL_RENDERBUFFER, buffernum)
    glUseProgram(program)
    glBindTexture(GL_TEXTURE_2D, 2)
    glShadeModel(GL_SMOOTH)
    glViewport(0, 0, size, size)
    glClearDepth(1.0)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(31.0, 1, 0.1, 30.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glTranslatef(0.0, 0.0, -10.0)
    glRotatef(view[0], 0.0, 1.0, 0.0)
    glRotatef(view[1], 1.0, 0.0, 0.0)
    glRotatef(view[2] + angle, 0.0, 0.0, 1.0)
    glColor3f(1, 0, 0)
    glutSolidTeapot(1.5)
    glUseProgram(0)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glBindTexture(GL_TEXTURE_2D, 0)


def CreateFrameBuffer(buffernumber, texturenumber):
    glGenFramebuffers(1)
    glGenRenderbuffers(1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texturenumber)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, "pixels")
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindFramebuffer(GL_FRAMEBUFFER, buffernumber)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texturenumber, 0)
    glBindRenderbuffer(GL_RENDERBUFFER, buffernumber)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, size, size)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, buffernumber)
    glBindRenderbuffer(GL_RENDERBUFFER, 0)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)


def InitGL(Width, Height):
    print "Vendor:   " + glGetString(GL_VENDOR)
    print "Renderer: " + glGetString(GL_RENDERER)
    print "OpenGL Version:  " + glGetString(GL_VERSION)
    print "Shader Version:  " + glGetString(GL_SHADING_LANGUAGE_VERSION)
    print "Max Framebuffers: ", glGetInteger(GL_MAX_COLOR_ATTACHMENTS)

    if not glUseProgram:
        print 'Missing Shader Objects!'
        sys.exit(1)

    global program
    program = compileProgram(
        compileShader('''
                varying vec2 texture_coordinate;
                void main()
                {
                    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                    texture_coordinate = vec2(gl_MultiTexCoord0);
                }
        ''', GL_VERTEX_SHADER),
        compileShader('''
                varying vec2 texture_coordinate; uniform sampler2D my_color_texture;
                uniform float myUniform;
                void main()
                {
                    vec4 color = texture2D(my_color_texture, texture_coordinate);
                    if (color.r > 0.9 && (color.r > 0.9 && color.b > 0.9))
                        discard;
                    gl_FragColor = vec4(gl_FragCoord.x/1024.0,myUniform,gl_FragCoord.y/102.0,1.0);
                }
    ''', GL_FRAGMENT_SHADER),
    )

    global program2
    program2 = compileProgram(
        compileShader('''
                varying vec2 texture_coordinate;
                void main()
                {
                    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                    texture_coordinate = vec2(gl_MultiTexCoord0);
                }
        ''', GL_VERTEX_SHADER),
        compileShader('''
                varying vec2 texture_coordinate; uniform sampler2D my_color_texture;
                uniform float myUniform;
                void main()
                {
                    vec4 color = texture2D(my_color_texture, texture_coordinate);
                    gl_FragColor = vec4(gl_FragCoord.x/1024.0,gl_FragCoord.y/1024.0,myUniform,1.0);
                    if (color.r > 0.9 && (color.r > 0.9 && color.b > 0.9))
                        discard;
                }
    ''', GL_FRAGMENT_SHADER),
    )

    #bmp texture 1
    image = open("rgb.bmp")
    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, 2)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

    CreateFrameBuffer(1, 3)
    CreateFrameBuffer(2, 4)
    CreateFrameBuffer(3, 5)
    CreateFrameBuffer(4, 6)


def DrawGLScene():
    global angle
    global frames

    DrawTeapot([90, 0, 0], angle, 1)
    DrawTeapot([0, 90, 0], angle, 2)
    DrawTeapot([0, 0, 90], angle, 3)
    DrawTeapot([45, 45, 0], angle, 4)

    if shadernumber == 0:
        glUseProgram(0)
    if shadernumber == 1:
        glUseProgram(program2)

    glEnable(GL_TEXTURE_2D)
    glViewport(0, 0, size, size)
    glClearDepth(1.0)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -30.0, 30.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glColor3f(0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, 3)
    drawQuad(0.0, 1.0, 0.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, 4)
    drawQuad(-1.0, 0.0, 0.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, 5)
    drawQuad(0.0, 1.0, -1.0, 0.0)
    glBindTexture(GL_TEXTURE_2D, 6)
    drawQuad(-1.0, 0.0, -1.0, 0.0)

    glFlush()
    glutSwapBuffers()
    angle += 0.5


def keyPressed(*args):
    global shadernumber
    if args[0] == ESCAPE:
        sys.exit()
    if args[0] == 's':
        if shadernumber == 1:
            shadernumber = 0
        else:
            shadernumber = 1


def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(size, size)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Rendering to 4 textures(+shader) then display on 4 quads(+shader2)")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(size, size)
    glutMainLoop()

if __name__ == "__main__":
    print "Press 'ESC' key to quit."
    print "press 's' to activate 2nd shader"
    main()
