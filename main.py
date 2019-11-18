'''
@Author: Alicespace
@Date: 2019-11-18 08:06:30
@LastEditTime: 2019-11-18 13:28:18
'''
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3


class stellarMovementSimulator(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)


app = stellarMovementSimulator()
app.run()
