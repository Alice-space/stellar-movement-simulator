'''
@Author: Alicespace
@Date: 2019-12-09 15:33:13
@LastEditTime: 2019-12-09 15:42:45
'''
import finalcalculation as c
import MEM
MEM.createobject(mass=10, cor=[-50, 0, 0], vel=[0, -60, 0])
MEM.createobject(mass=10, cor=[100, 0, 0], vel=[0, 70, 0])
MEM.createobject(mass=200, cor=[-30, 0, 0], vel=[0, 110, 0])
MEM.createobject(mass=200, cor=[15, 0, 0], vel=[0, -110, 0])
MEM.createobject(mass=300, cor=[21, 34, 0], vel=[0, -10, 0])
c.calculate(delta_t=10)

print(MEM.getobjects()[1].dataOUT())
MEM.getobjects()[1].objdata = []
# t vx vy vz x y z
