'''
@Author: Alicespace
@Date: 2019-11-18 08:06:30
@LastEditTime: 2019-11-19 22:01:38
'''
import sys
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, loadPrcFileData
from direct.actor.Actor import Actor
from direct.task import Task


class stellarMovementSimulator(ShowBase):
    '''
    @description:
        enter point of the main function
    @param {type}
        ShowBase {ShowBase}
    @return:
        null
    '''
    def __init__(self):
        # loadPrcFileData('', 'fullscreen true')
        loadPrcFile("res/config/Config.prc")
        ShowBase.__init__(self)
        # some properties about window and mouse
        self.disableMouse()

        # an earth model
        self.pandaActor = self.loader.loadModel("res/tmp/earth/earth")
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.setPos(0, 0, 0)
        self.taskMgr.add(self.moveCamera, "moveCamera")
        # store keyMap
        self.keyMap = {
            "left": 0,
            "right": 0,
            "forward": 0,
            "backward": 0,
            "up": 0,
            "down": 0
        }
        # add key events
        self.accept("q", sys.exit)
        self.accept("a", self.setKey, ["left", True])
        self.accept("d", self.setKey, ["right", True])
        self.accept("w", self.setKey, ["forward", True])
        self.accept("s", self.setKey, ["backward", True])
        self.accept("space", self.setKey, ["up", True])
        self.accept("lshift", self.setKey, ["down", True])
        self.accept("a-up", self.setKey, ["left", False])
        self.accept("d-up", self.setKey, ["right", False])
        self.accept("w-up", self.setKey, ["forward", False])
        self.accept("s-up", self.setKey, ["backward", False])
        self.accept("space-up", self.setKey, ["up", False])
        self.accept("lshift-up", self.setKey, ["down", False])

    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    # Define a procedure to move the camera.
    def moveCamera(self, task):
        dt = globalClock.getDt()
        # deal with movement events
        if self.keyMap["left"]:
            self.camera.setX(self.camera.getX() - 10 * dt)
        if self.keyMap["right"]:
            self.camera.setX(self.camera.getX() + 10 * dt)
        if self.keyMap["forward"]:
            self.camera.setY(self.camera.getY() + 10 * dt)
        if self.keyMap["backward"]:
            self.camera.setY(self.camera.getY() - 10 * dt)
        if self.keyMap["up"]:
            self.camera.setZ(self.camera.getZ() + 10 * dt)
        if self.keyMap["down"]:
            self.camera.setZ(self.camera.getZ() - 10 * dt)
        return task.cont


app = stellarMovementSimulator()
app.run()
