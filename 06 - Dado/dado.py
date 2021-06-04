import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from png import Reader
from sys import argv
from math import sin, cos, pi

# Window Name
window_name = "Dado Texturizado"

# Rotation vars
left_button = False
alpha = 90.0
beta = 0
delta_alpha = 0.5

# Translation vars
right_button = False
delta_x, delta_y, delta_z = 0, 0, 0

down_x, down_y = 0, 0

# Colors

# Background Color RGBA
background_color = (0.184, 0.211, 0.250, 1)

# Figure vars

n = 50
m = 50
radius = 2

# Texture vars

texture = []

# Texture Functions

def load_textures():
    global texture
    texture = GL.glGenTextures(2)

    png_img = Reader(filename='dado.png')

    w, h, pixels, metadata = png_img.read_flat()

    if(metadata['alpha']):
        modo = GL.GL_RGBA
    else:
        modo = GL.GL_RGB

    GL.glBindTexture(GL.GL_TEXTURE_2D, texture[0])
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL.GL_UNSIGNED_BYTE, pixels.tolist())
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    GL.glTexEnvf(GL.GL_TEXTURE_ENV, GL.GL_TEXTURE_ENV_MODE, GL.GL_DECAL)


def figure():
    
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)    
    GL.glLoadIdentity()    
    
    GL.glPushMatrix()

    # Translation and Zoom
    GL.glTranslatef(delta_x, delta_y, delta_z)

    # Rotation
    # X axis
    GL.glRotatef(alpha, 1.0, 1.0, 0.0)
    # Y axis
    GL.glRotatef(beta, 1.0, 1.0, 1.0)

    # Figure
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture[0])
    GL.glBegin(GL.GL_QUADS)

    # Front Face
    GL.glTexCoord2f(0.0, 0.0); GL.glVertex3f(-1.0, -1.0,  1.0)
    GL.glTexCoord2f(1/3, 0.0); GL.glVertex3f( 1.0, -1.0,  1.0)
    GL.glTexCoord2f(1/3, 1/2); GL.glVertex3f( 1.0,  1.0,  1.0)
    GL.glTexCoord2f(0.0, 1/2); GL.glVertex3f(-1.0,  1.0,  1.0)  

    # Back Face
    GL.glTexCoord2f(2/3, 1/2); GL.glVertex3f(-1.0, -1.0, -1.0)
    GL.glTexCoord2f(1.0, 1/2); GL.glVertex3f(-1.0,  1.0, -1.0)
    GL.glTexCoord2f(1.0, 1.0); GL.glVertex3f( 1.0,  1.0, -1.0)
    GL.glTexCoord2f(2/3, 1.0); GL.glVertex3f( 1.0, -1.0, -1.0) 
    
    # Top Face
    GL.glTexCoord2f(1/3, 1/2); GL.glVertex3f(-1.0,  1.0, -1.0)
    GL.glTexCoord2f(2/3, 1/2); GL.glVertex3f(-1.0,  1.0,  1.0)
    GL.glTexCoord2f(2/3, 1); GL.glVertex3f( 1.0,  1.0,  1.0)
    GL.glTexCoord2f(1/3, 1); GL.glVertex3f( 1.0,  1.0, -1.0)  

    # Bottom Face       
    GL.glTexCoord2f(1/3, 0.0); GL.glVertex3f(-1.0, -1.0, -1.0)
    GL.glTexCoord2f(2/3, 0.0); GL.glVertex3f( 1.0, -1.0, -1.0)
    GL.glTexCoord2f(2/3, 1/2); GL.glVertex3f( 1.0, -1.0,  1.0)
    GL.glTexCoord2f(1/3, 1/2); GL.glVertex3f(-1.0, -1.0,  1.0)    
    
    # Right face
    GL.glTexCoord2f(0.0, 1/2); GL.glVertex3f( 1.0, -1.0, -1.0)
    GL.glTexCoord2f(1/3, 1/2); GL.glVertex3f( 1.0,  1.0, -1.0)
    GL.glTexCoord2f(1/3, 1.0); GL.glVertex3f( 1.0,  1.0,  1.0)
    GL.glTexCoord2f(0.0, 1.0); GL.glVertex3f( 1.0, -1.0,  1.0) 
    
    # Left Face
    GL.glTexCoord2f(2/3, 0.0); GL.glVertex3f(-1.0, -1.0, -1.0)
    GL.glTexCoord2f(1.0, 0.0); GL.glVertex3f(-1.0, -1.0,  1.0)
    GL.glTexCoord2f(1.0, 1/2); GL.glVertex3f(-1.0,  1.0,  1.0)
    GL.glTexCoord2f(2/3, 1/2); GL.glVertex3f(-1.0,  1.0, -1.0)  
    
    GL.glEnd()

    GL.glPopMatrix()

    GLUT.glutSwapBuffers()


def draw():
    global alpha

    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    figure()

    # Auto-Rotation
    alpha = alpha + delta_alpha

    GLUT.glutSwapBuffers()


def timer(i):
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(10, timer, 1)

def main():    
    GLUT.glutInit(argv)
    GLUT.glutInitDisplayMode(
        GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH | GLUT.GLUT_MULTISAMPLE
    )

    # Creating a screen with good resolution proportions
    screen_width = GLUT.glutGet(GLUT.GLUT_SCREEN_WIDTH)
    screen_height = GLUT.glutGet(GLUT.GLUT_SCREEN_HEIGHT)

    window_width = round(2 * screen_width / 3)
    window_height = round(2 * screen_height / 3)

    GLUT.glutInitWindowSize(window_width, window_height)
    GLUT.glutInitWindowPosition(
        round((screen_width - window_width) / 2), round((screen_height - window_height) / 2)
    )
    GLUT.glutCreateWindow(window_name)

    # Drawing Function
    GLUT.glutDisplayFunc(draw)

    load_textures()

    GL.glEnable(GL.GL_MULTISAMPLE)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_TEXTURE_2D)

    GL.glClearColor(*background_color)
    GL.glClearDepth(1.0)
    GL.glDepthFunc(GL.GL_LESS)

    GL.glShadeModel(GL.GL_SMOOTH)
    GL.glMatrixMode(GL.GL_PROJECTION)

    # Pre-render camera positioning
    GLU.gluPerspective(-45, window_width / window_height, 0.1, 100.0)
    GL.glTranslatef(0.0, 0.0, -10)

    GL.glMatrixMode(GL.GL_MODELVIEW)

    GLUT.glutTimerFunc(10, timer, 1)
    GLUT.glutMainLoop()


if(__name__ == '__main__'):
    main()