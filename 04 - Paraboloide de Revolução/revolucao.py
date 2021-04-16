import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from sys import argv
from math import sin, cos, pi

window_name = "Paraboloide de Revolucao"

# Rotation vars
left_button = False
alpha = 0
beta = 180.0
delta_alpha = 0.5

# Translation vars
right_button = False
delta_x, delta_y, delta_z = 0, 0, 0

down_x, down_y = 0, 0

# Cores

# Background Color RGBA
background_color = (0.384, 0.411, 0.450, 1)

# Figure Vars
m, n = 20, 20
radius = 2

# Figure functions
def f(i,j):
    
    theta = ( (pi * i) / (m -1) ) - (pi / 2)
    phi = 2*pi*j/(n-1)
    
    x = radius * cos(theta) * cos(phi)
    y = radius * sin(theta)
    z = radius * cos(theta) * sin(phi)
    
    return x, y**2, z

def figure():
    GL.glPushMatrix()

    # Translation and Zoom
    GL.glTranslatef(delta_x, delta_y + 1.5, delta_z)

    # Rotation
    # X axis
    GL.glRotatef(alpha, 0.0, 1.0, 0.0)
    # Y axis
    GL.glRotatef(beta, 0.0, 0.0, 1.0)

    # Figure
    for i in range(round(m/2)):
        GL.glBegin(GL.GL_QUAD_STRIP)
        for j in range(n):
            GL.glColor3fv(((1.0*i/(m-1)), 0, 1 - (1.0*i/(m-1))))

            x, y, z = f(i,j)
            GL.glVertex3f(x,y,z)
            
            GL.glColor3fv(((1.0*(i+1)/(m-1)), 0, 1 - (1.0*(i+1)/(m-1))))
            x, y, z = f(i+1, j)
            GL.glVertex3f(x,y,z)
        GL.glEnd()
    GL.glPopMatrix()

def draw():
    global alpha, left_button, right_button
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

    GL.glEnable(GL.GL_MULTISAMPLE)
    GL.glEnable(GL.GL_DEPTH_TEST)

    GL.glClearColor(*background_color)

    # Pre-render camera positioning
    GLU.gluPerspective(-45, window_width / window_height, 0.1, 100.0)
    GL.glTranslatef(0.0, 0.0, -10)

    GLUT.glutTimerFunc(10, timer, 1)
    GLUT.glutMainLoop()

if(__name__ == '__main__'):
    main()