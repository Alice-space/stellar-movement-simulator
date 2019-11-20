'''
@Author: Alicespace
@Date: 2019-11-18 08:06:30
@LastEditTime: 2019-11-20 14:16:06
'''

import sys
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, loadPrcFileData
from direct.actor.Actor import Actor
from direct.task import Task


class cameraSpeed():
    '''
    @description:
    a class for velocity change and effect
    @param {type}
    null
    @return:
    null
    '''
    defaultMoveSpeed = 10
    minVelocity = 0.001
    velocityDecayRate = 0.5
    Vx = 0
    Vy = 0
    Vz = 0

    def addVx(self, dt):
        cameraSpeed.Vx += self.defaultMoveSpeed * dt

    def addVy(self, dt):
        cameraSpeed.Vy += self.defaultMoveSpeed * dt

    def addVz(self, dt):
        cameraSpeed.Vz += self.defaultMoveSpeed * dt

    def slideX(self):
        if (abs(cameraSpeed.Vx) <= self.minVelocity):
            cameraSpeed.Vx = 0
        if (cameraSpeed.Vx != 0):
            cameraSpeed.Vx *= self.velocityDecayRate

    def slideY(self):
        if (abs(cameraSpeed.Vy) <= self.minVelocity):
            cameraSpeed.Vy = 0
        if (cameraSpeed.Vy != 0):
            cameraSpeed.Vy *= self.velocityDecayRate

    def slideZ(self):
        if (abs(cameraSpeed.Vz) <= self.minVelocity):
            cameraSpeed.Vz = 0
        if (cameraSpeed.Vz != 0):
            cameraSpeed.Vz *= self.velocityDecayRate


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

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # an earth model
        self.pandaActor = self.loader.loadModel("res/tmp/earth/earth")
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.setPos(0, 0, 0)

        # add camera move task
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

        # instance a speed object
        self.cameraSpeed = cameraSpeed()

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
        isXMoved = False
        isYMoved = False
        isZMoved = False

        # judge movement
        if self.keyMap["left"]:
            if self.cameraSpeed.Vx > 0:
                self.cameraSpeed.slideX()
            self.cameraSpeed.addVx(-dt)
            isXMoved = True
        if self.keyMap["right"]:
            if self.cameraSpeed.Vx < 0:
                self.cameraSpeed.slideX()
            self.cameraSpeed.addVx(dt)
            isXMoved = True
        if self.keyMap["forward"]:
            if self.cameraSpeed.Vy < 0:
                self.cameraSpeed.slideY()
            self.cameraSpeed.addVy(dt)
            isYMoved = True
        if self.keyMap["backward"]:
            if self.cameraSpeed.Vy > 0:
                self.cameraSpeed.slideY()
            self.cameraSpeed.addVy(-dt)
            isYMoved = True
        if self.keyMap["up"]:
            if self.cameraSpeed.Vz < 0:
                self.cameraSpeed.slideZ()
            self.cameraSpeed.addVz(dt)
            isZMoved = True
        if self.keyMap["down"]:
            if self.cameraSpeed.Vz > 0:
                self.cameraSpeed.slideZ()
            self.cameraSpeed.addVz(-dt)
            isZMoved = True
        if not isXMoved:
            self.cameraSpeed.slideX()
        if not isYMoved:
            self.cameraSpeed.slideY()
        if not isZMoved:
            self.cameraSpeed.slideZ()
        self.camera.setPos(self.camera.getX() + self.cameraSpeed.Vx,
                           self.camera.getY() + self.cameraSpeed.Vy,
                           self.camera.getZ() + self.cameraSpeed.Vz)
        return task.cont


app = stellarMovementSimulator()
app.run()
