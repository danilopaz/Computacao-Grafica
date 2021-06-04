import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from sys import argv
from math import sin, cos, pi, sqrt

# Window Name
window_name = "Iluminacao dos Tronco da Pirâmide"

# Background Color RGBA
background_color = (0.184, 0.211, 0.250, 1)

# Figure Vars
vertices = 5
radius = 2
prism_height = 3
piramid_modifier = 1
X = 0
Y = 1
Z = 2

light_position = (10, 0, 0)
count = 0

# Illumination
materials = [
    #Brass
    [
    (0.329412, 0.223529, 0.027451,  1.0),
    (0.780392, 0.568627, 0.113725, 1.0),
    (0.992157, 0.941176, 0.807843, 1.0),
    (27.8974)
    ],         
    #Bronze
    [
        (0.2125, 0.1275, 0.054, 1.0),
        (0.714, 0.4284, 0.18144, 1.0),
        (0.393548, 0.271906, 0.166721, 1.0),
        (25.6)
    ]
]
#Fonte: http://www.it.hiof.no/~borres/j3d/explain/light/p-materials.html



# Figure Functions
def calcula_normal(v0, v1, v2):
    U = (v2[X]-v0[X], v2[Y]-v0[Y], v2[Z]-v0[Z])
    V = (v1[X]-v0[X], v1[Y]-v0[Y], v1[Z]-v0[Z])
    N = ((U[Y]*V[Z]-U[Z]*V[Y]),(U[Z]*V[X]-U[X]*V[Z]),(U[X]*V[Y]-U[Y]*V[X]))
    normal_length = sqrt(N[X]*N[X]+N[Y]*N[Y]+N[Z]*N[Z])
    return (N[X]/normal_length, N[Y]/normal_length, N[Z]/normal_length)


def calcula_normal_invertida(v0, v1, v2):
    U = ( v2[X]-v0[X], v2[Y]-v0[Y], v2[Z]-v0[Z] )
    V = ( v1[X]-v0[X], v1[Y]-v0[Y], v1[Z]-v0[Z] )
    N = ( (U[Y]*V[Z]-U[Z]*V[Y]),(U[Z]*V[X]-U[X]*V[Z]),(U[X]*V[Y]-U[Y]*V[X]))
    normal_length = sqrt(N[X]*N[X]+N[Y]*N[Y]+N[Z]*N[Z])
    return (-N[X]/normal_length, -N[Y]/normal_length, -N[Z]/normal_length)


def figure():

    polygon_points = []
    faces_angle = (2*pi)/vertices
    
    GL.glPushMatrix()
    
    GL.glTranslatef(0.0, -1.0, 0.0)
    GL.glRotatef(-100,1.0,0.0,0.0)
  
    # Figure

    # Bottom
    GL.glBegin(GL.GL_POLYGON)
    for i in range(vertices):
        x = radius * cos(i*faces_angle)
        y = radius * sin(i*faces_angle)
        polygon_points += [ (x,y) ]
        GL.glVertex3f(x,y,0.0)
    
    u = (polygon_points[0][0], polygon_points[0][1], 0)
    v = (polygon_points[1][0], polygon_points[1][1], 0)
    p = (polygon_points[2][0], polygon_points[2][1], 0)

    #Por algum motivo, se eu uso a calcula_normal a iluminação inverte: acende quando deveria apagar e apaga quando deveria acender.
    GL.glNormal3fv(calcula_normal_invertida(u,v,p))
    GL.glEnd()

    # Top
    GL.glBegin(GL.GL_POLYGON)
    for x,y in polygon_points:
        GL.glVertex3f(piramid_modifier*x,piramid_modifier*y, prism_height)
    
    u = (polygon_points[0][0], polygon_points[0][1], prism_height)
    v = (polygon_points[1][0], polygon_points[1][1], prism_height)
    p = (polygon_points[2][0], polygon_points[2][1], prism_height)

    GL.glNormal3fv(calcula_normal(u,v,p))
    GL.glEnd()

    # Sides
    GL.glBegin(GL.GL_QUADS)
    for i in range(vertices):
        u = (polygon_points[i][0],polygon_points[i][1],0)
        v = (piramid_modifier*polygon_points[i][0],piramid_modifier*polygon_points[i][1],prism_height)
        p = (piramid_modifier*polygon_points[(i+1)%vertices][0],piramid_modifier*polygon_points[(i+1)%vertices][1],prism_height)
        q = (polygon_points[(i+1)%vertices][0],polygon_points[(i+1)%vertices][1],0)

        GL.glNormal3fv(calcula_normal(u,v,q))
        
        GL.glVertex3fv(u)
        GL.glVertex3fv(v)
        GL.glVertex3fv(p)
        GL.glVertex3fv(q)
    GL.glEnd()

    GL.glPopMatrix()


def draw():
    global count

    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glRotatef(2,1,3,0)

    #Material
    if count % 150 == 0:
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT, materials[(count+1)%len(materials)][0])
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, materials[(count+1)%len(materials)][1])
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, materials[(count+1)%len(materials)][2])
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, materials[(count+1)%len(materials)][3])
    count += 1

    figure()

    GLUT.glutSwapBuffers()


def timer(i):
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(50, timer, 1)

def reshape(w,h):
    GL.glViewport(0,0,w,h)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GLU.gluPerspective(45, float(w) / float(h), 0.1, 50.0)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()

    GLU.gluLookAt(10,0,0,0,0,0,0,1,0)
    

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

    # Reshape Function
    GLUT.glutReshapeFunc(reshape)

    # Drawing Function
    GLUT.glutDisplayFunc(draw)
    
    #GL.glShadeModel(GL.GL_FLAT)
    GL.glShadeModel(GL.GL_SMOOTH)

    #First Material
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT, materials[0][0])
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, materials[0][1])
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, materials[0][2])
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, materials[0][3])

    GL.glEnable(GL.GL_LIGHTING)
    GL.glEnable(GL.GL_LIGHT0)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)

    GL.glEnable(GL.GL_MULTISAMPLE)
    GL.glEnable(GL.GL_DEPTH_TEST)

    GL.glClearColor(*background_color)

    # Pre-render camera positioning
    GLU.gluPerspective(45, window_width / window_height, 0.1, 50.0)


    GLUT.glutTimerFunc(50, timer, 1)
    GLUT.glutMainLoop()


if(__name__ == '__main__'):
    main()