from Tello_Drone2 import *

tello_list = []
color = ['red', 'gold', 'blue', 'green', 'c']
for i in range(5):
    temp = Drone(color[i])
    tello_list.append(temp)
tello = Drone_fly(tello_list=tello_list)


def buttonfunc():
    exit()

bu = tello.vp.addButton(
    fnc=buttonfunc,
    pos=[0.5, 0.05],
    states=["Close"],
    c=["w"],
    bc=["dg"],
    size=20,
    bold=True,
    italic=False
)

tello.up(height=5, drone_list=[2], speed=0.5)
tello.up(height=5, drone_list=[4], speed=0.5)
tello.up(height=5, drone_list=[1,3,5], speed=0.5)
tello.back(distance=8, drone_list=[1], speed=0.5)
tello.forward(distance=8, drone_list=[5], speed=0.5)
tello.right(distance=24, drone_list=[1], speed=0.5)
tello.left(distance=24, drone_list=[5], speed=0.5)
tello.back(distance=8, drone_list=[1],speed=0.5)
tello.up(height=3, drone_list=[1],speed=0.5)
tello.left(distance=12, drone_list=[2],speed=0.5)
tello.up(height=3, drone_list=[2],speed=0.5)
tello.right(distance=12, drone_list=[4],speed=0.5)
tello.up(height=3, drone_list=[4],speed=0.5)
tello.forward(distance=8, drone_list=[5],speed=0.5)
tello.up(height=3, drone_list=[5],speed=0.5)
tello.right(distance=8, drone_list=[1],speed=0.5)
tello.forward(distance=4, drone_list=[1],speed=0.5)
tello.back(distance=8, drone_list=[2],speed=0.5)
tello.right(distance=12, drone_list=[2],speed=0.5)
tello.forward(distance=8, drone_list=[4],speed=0.5)
tello.left(distance=12, drone_list=[4],speed=0.5)
tello.left(distance=8, drone_list=[5],speed=0.5)
tello.back(distance=4, drone_list=[5],speed=0.5)
tello.right(distance=12, drone_list=[1],speed=0.5)
tello.forward(distance=12, drone_list=[1],speed=0.5)
tello.back(distance=4, drone_list=[2],speed=0.5)
tello.right(distance=12, drone_list=[2],speed=0.5)
tello.forward(distance=4, drone_list=[4],speed=0.5)
tello.left(distance=12, drone_list=[4],speed=0.5)
tello.left(distance=12, drone_list=[5],speed=0.5)
tello.back(distance=12, drone_list=[5],speed=0.5)
tello.right(distance=4, drone_list=[1],speed=0.5)
tello.left(distance=4, drone_list=[5],speed=0.5)
tello.up(height=3, drone_list=[3],speed=0.5)
tello.right(distance=12, drone_list=[2],speed=0.5)
tello.forward(distance=12, drone_list=[2],speed=0.5)
tello.left(distance=12, drone_list=[4],speed=0.5)
tello.back(distance=12, drone_list=[4],speed=0.5)
tello.down(height=3, drone_list=[5],speed=0.5)
tello.down(height=3, drone_list=[4],speed=0.5)
tello.up(height=3, drone_list=[5],speed=0.5)
tello.down(height=3, drone_list=[3],speed=0.5)
tello.up(height=3, drone_list=[4],speed=0.5)
tello.down(height=3, drone_list=[2],speed=0.5)
tello.up(height=3, drone_list=[3],speed=0.5)
tello.down(height=3, drone_list=[1],speed=0.5)
tello.up(height=3, drone_list=[2],speed=0.5)
tello.up(height=3, drone_list=[1],speed=0.5)
tello.down(height=5, drone_list=[1,3,5],speed=0.5)
tello.down(height=5, drone_list=[2,4],speed=0.5)

interactive()
