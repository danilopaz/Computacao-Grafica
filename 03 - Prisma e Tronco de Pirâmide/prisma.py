import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from sys import argv
from math import sin, cos, pi

window_name = "Prisma"

left_button = False
alpha = 0
beta = 0
delta_alpha = 0.5

right_button = False
delta_x, delta_y, delta_z = 0, 0, 0

down_x, down_y = 0, 0

# Cores
sides_colors = (
    (0.700, 0.132, 0.512),
    (0.298, 0.819, 0.215),
    (0, 0.658, 1),
    (0.123,0.213,0.745),
    (0.435,0.326,0.777)
)

top_bottom_colors = (0.862, 0.866, 0.882)

# Background Color RGBA
background_color = (0.384, 0.411, 0.450, 1)

# Figure Vars

vertices = 5
radius = 2
prism_height = 3

def figure():

    polygon_points = []
    faces_angle = (2*pi)/vertices
    
    GL.glPushMatrix()
    
    GL.glTranslatef(0.0, 1.5, -10)
    GL.glRotatef(90,1.0,0.0,1.5)

    # Translation and Zoom
    GL.glTranslatef(delta_x, delta_y, delta_z)

    # Rotation
    # X axis
    GL.glRotatef(alpha, 0.0, 0.0, 1.0)
    # Y axis
    GL.glRotatef(beta, 0.0, 1.0, 0.0)

    # Bottom
    GL.glColor3fv(top_bottom_colors)
    GL.glBegin(GL.GL_POLYGON)
    for i in range(vertices):
        x = radius * cos(i*faces_angle)
        y = radius * sin(i*faces_angle)
        polygon_points += [ (x,y) ]
        GL.glVertex3f(x,y,0.0)
    GL.glEnd()

    # Top
    GL.glBegin(GL.GL_POLYGON)
    for x,y in polygon_points:
        GL.glVertex3f(x,y, prism_height)
    GL.glEnd()

    # Sides
    GL.glBegin(GL.GL_QUADS)
    for i in range(vertices):
        GL.glColor3fv(sides_colors[i%5])
        
        GL.glVertex3f(polygon_points[i][0],polygon_points[i][1],0)
        GL.glVertex3f(polygon_points[i][0],polygon_points[i][1],prism_height)

        GL.glVertex3f(polygon_points[(i+1)%vertices][0],polygon_points[(i+1)%vertices][1],prism_height)
        GL.glVertex3f(polygon_points[(i+1)%vertices][0],polygon_points[(i+1)%vertices][1],0)
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


    GLUT.glutTimerFunc(10, timer, 1)
    GLUT.glutMainLoop()


if(__name__ == '__main__'):
    main()