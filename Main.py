from Tello_Drone import *
from MainPage import MainPageWindow
from PyQt5.QtWidgets import QApplication
import sys
from vedo import *


if __name__ == '__main__':
    app = QApplication(sys.argv)

    tello_list = []
    color = ['red', 'gold', 'blue', 'green', 'c']
    for i in range(5):
        temp = Drone(color[i])
        tello_list.append(temp)

    mainWindow = MainPageWindow()
    vp = Plotter(qtWidget=mainWindow.vtkWidget)
    world = Box(pos=[0, 0, 0], length=64, width=36, height=20).wireframe()
    template_drone = load('resources/model/dobby03.stl').normalize().rotateZ(-90).addTrail()
    drone_list = []
    drone_tag = []
    for num in range(len(tello_list)):
        drone_list.append(template_drone.clone().pos(x=5 * (num - 2), y=0, z=0)
                          .color(tello_list[num - 1].color))
        drone_tag.append(Marker(pos=[5 * (num - 2), 0, 1.5], symbol='#0' + str(num + 1)).scale(5)
                         .color(tello_list[num - 1].color))
    vp.show(world, drone_list, drone_tag, axes=1, viewup='z', interactive=0)
    mainWindow.show()

    app.aboutToQuit.connect(mainWindow.vtk_close)
    sys.exit(app.exec_())
