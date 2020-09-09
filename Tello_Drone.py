from vedo import *
from math import pi


# 针对单个无人机的属性创建类
class Drone():
    def __init__(self, color='gold', yaw=-90, x=0, y=0, z=0):
        self.color = color
        self.yaw = yaw
        self.x = x
        self.y = y
        self.z = z

    def update_yaw(self, angle):
        self.yaw += angle
        if self.yaw > 360:
            self.yaw -= 360
        elif self.yaw < 0:
            self.yaw += 360


# 针对无人机的操作进行定义
class Drone_fly():
    def __init__(self, vtkWidget, tello_list: list = []):
        self.vp = Plotter(qtWidget=vtkWidget, bg='light gray')
        self.world = Box(pos=[0, 0, 0], length=64, width=36, height=20).wireframe()
        template_drone = load('resources/model/dobby03.stl').normalize().rotateZ(-90).addTrail()
        # text = Marker(pos=[0, 0, 5], symbol='01').scale(5).rotateX(90)
        self.drone_para = tello_list
        self.drone_list = []
        self.drone_tag = []
        for num in range(len(tello_list)):
            self.drone_list.append(template_drone.clone().pos(x=5*(num-2), y=0, z=0)
                                   .color(self.drone_para[num-1].color))
            self.drone_tag.append(Marker(pos=[5*(num-2), 0, 1.5], symbol='#0' + str(num+1)).scale(5)
                                  .color(self.drone_para[num-1].color))
        self.vp.show(self.world, self.drone_list, self.drone_tag, axes=1, viewup='z', interactive=0)

    def drone_translate(self, x: float = 0, y: float = 0, z: float = 0, drone_list: list = [], sync: bool = True):
        if len(drone_list) == 0:
            for i in range(len(self.drone_list)):
                self.drone_list[i].addPos(x, y, z)
                self.drone_tag[i].addPos(x, y, z)
        else:
            for i in drone_list:
                self.drone_list[i-1].addPos(x, y, z)
                self.drone_tag[i-1].addPos(x, y, z)
        if sync:
            self.update()

    def drone_rotate(self, yaw: float = 0, pitch: float = 0, roll: float = 0, drone_list: list = [], sync: bool = True):
        if len(drone_list) == 0:
            for i in range(len(self.drone_list)):
                [x, y, z] = list(self.drone_list[i].pos())
                self.drone_list[i].rotate(angle=yaw, axis=(0, 0, 1), axis_point=(x, y, z))
                self.drone_tag[i].rotate(angle=yaw, axis=(0, 0, 1), axis_point=(x, y, z))
        else:
            for i in drone_list:
                [x, y, z] = list(self.drone_list[i-1].pos())
                self.drone_list[i-1].rotate(angle=yaw, axis=(0, 0, 1), axis_point=(x, y, z))
                self.drone_tag[i-1].rotate(angle=yaw, axis=(0, 0, 1), axis_point=(x, y, z))
        if sync:
            self.update()

    # Transform from body axis to world axis
    def coordinate(self, x: float = 0, y: float = 0, yaw: float = 0):
        angle = yaw / 180 * pi
        x_worldaxis = cos(angle) * x + sin(angle) * y
        y_worldaxis = -sin(angle) * x + cos(angle) * y
        return [x_worldaxis, y_worldaxis]

    def update(self):
        self.vp.interactor.Render()

    def up(self, height: float = 0, drone_list: list = [], speed: float = 5):
        if len(drone_list) == 0:
            for t in arange(0, height, height/100*speed):
                self.drone_translate(z=height/100*speed)
        else:
            for t in arange(0, height, height/100*speed):
                self.drone_translate(z=height/100*speed, drone_list=drone_list)

    def down(self, height: float = 0, drone_list: list = [], speed: float = 5):
        self.up(height=-height, drone_list=drone_list, speed=speed)

    def left(self, distance: float = 0, drone_list: list = [], speed: float = 5):
        x = []
        y = []
        for drone in self.drone_para:
            [temp_x, temp_y] = self.coordinate(x=0, y=distance, yaw=drone.yaw)
            x.append(temp_x)
            y.append(temp_y)
        if len(drone_list) == 0:
            for t in arange(0, distance, distance / 100 * speed):
                for i in range(len(self.drone_list)):
                    self.drone_translate(x=x[i] / 100 * speed, y=y[i] / 100 * speed, drone_list=[i + 1], sync=False)
                self.update()
        else:
            for t in arange(0, distance, distance / 100 * speed):
                for i in drone_list:
                    self.drone_translate(x=x[i - 1] / 100 * speed, y=y[i - 1] / 100 * speed, drone_list=[i], sync=False)
                self.update()

    def right(self, distance: float = 0, drone_list: list = [], speed: float = 5):
        self.left(distance=-distance, drone_list=drone_list, speed=speed)

    def forward(self, distance: float = 0, drone_list: list = [], speed: float = 5):
        x = []
        y = []
        for drone in self.drone_para:
            [temp_x, temp_y] = self.coordinate(x=distance, y=0, yaw=drone.yaw)
            x.append(temp_x)
            y.append(temp_y)
        if len(drone_list) == 0:
            for t in arange(0, distance, distance/100*speed):
                for i in range(len(self.drone_list)):
                    self.drone_translate(x=x[i]/100*speed, y=y[i]/100*speed, drone_list=[i+1], sync=False)
                self.update()
        else:
            for t in arange(0, distance, distance/100*speed):
                for i in drone_list:
                    self.drone_translate(x=x[i-1]/100*speed, y=y[i-1]/100*speed, drone_list=[i], sync=False)
                self.update()

    def back(self, distance: float = 0, drone_list: list = [], speed: float = 5):
        self.forward(distance=-distance, drone_list=drone_list, speed=speed)

    def cw(self, yaw: float = 0, drone_list: list = [], speed: float = 5):
        if len(drone_list) == 0:
            for t in arange(0, yaw, yaw/100*speed):
                self.drone_rotate(yaw=-yaw/100*speed)
            for drone in self.drone_para:
                drone.update_yaw(yaw)
        else:
            for t in arange(0, yaw, yaw/100*speed):
                self.drone_rotate(yaw=-yaw/100*speed, drone_list=drone_list)
            for i in drone_list:
                self.drone_para[i-1].update_yaw(yaw)

    def ccw(self, yaw: float = 0, drone_list: list = [], speed: float = 5):
        self.cw(yaw=-yaw, drone_list=drone_list, speed=speed)