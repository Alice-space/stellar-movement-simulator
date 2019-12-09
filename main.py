'''
@Author: Alicespace
@Date: 2019-11-18 08:06:30
@LastEditTime: 2019-12-09 16:51:27
'''

import sys
from math import pi, sin, cos
from starDB import starDBManger
from calculate import finalcalculation
from calculate import Mem
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import loadPrcFile, loadPrcFileData, WindowProperties, Texture, TextureStage, DirectionalLight, AmbientLight, TexGenAttrib
from direct.actor.Actor import Actor
from direct.task import Task
# from pandac.PandaModules import WindowProperties, Texture, TextureStage, DirectionalLight, AmbientLight, TexGenAttrib
table_name = 'Star_info'

Actors = []


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
        loadPrcFileData('', 'fullscreen false')
        ShowBase.__init__(self)
        self.base = self
        self.setup()

    def setup(self):
        # some properties about window and mouse
        self.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        self.base.win.requestProperties(props)
        # db
        self.db = starDBManger.DBTool(table_name)
        self.loadmodels()

        # add camera move task
        self.taskMgr.add(self.moveCamera, "moveCamera")
        self.taskMgr.add(self.skysphereTask, "SkySphere Task")
        self.taskMgr.add(self.spinCamera, "spinCamera")
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
        self.accept("q", self.quitMain)
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

        # load sky sphere
        self.skysphere = self.loader.loadModel("res/skyBg/InvertedSphere.egg")
        self.skysphere.setTexGen(TextureStage.getDefault(),
                                 TexGenAttrib.MWorldPosition)
        self.skysphere.setTexProjector(TextureStage.getDefault(), self.render,
                                       self.skysphere)
        self.skysphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.skysphere.setTexScale(TextureStage.getDefault(), .5)
        tex = self.loader.loadCubeMap("res/skyBg/BlueGreenNebula__#.png")
        self.skysphere.setTexture(tex)
        self.skysphere.setLightOff()
        self.skysphere.setScale(1000)
        self.skysphere.reparentTo(self.render)
        self.skysphere.setBin('background', 1)
        self.skysphere.setDepthWrite(0)
        self.skysphere.reparentTo(self.render)

        global prevMouseX
        global prevMouseY
        global prevMouseVal
        global prevDxs
        global prevDys
        global totalSmoothStore
        prevMouseVal = 0
        prevMouseX = 0
        prevMouseY = 0
        prevDxs = []
        prevDys = []
        totalSmoothStore = 10

        self.mainSequence = Sequence()

    def quitMain(self):
        self.db.close()
        sys.exit()

    def skysphereTask(self, task):
        self.skysphere.setPos(self.camera, 0, 0, 0)
        return task.cont

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
        '''
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
        '''
        if not isXMoved:
            self.cameraSpeed.slideX()
        if not isYMoved:
            self.cameraSpeed.slideY()
        '''
        if not isZMoved:
            self.cameraSpeed.slideZ()
        '''
        self.camera.setX(self.camera, self.cameraSpeed.Vx * 0.5)
        self.camera.setY(self.camera, self.cameraSpeed.Vy)
        return task.cont

    def spinCamera(self, task):
        global prevMouseX
        global prevMouseY
        global prevMouseVal
        global prevDxs
        global prevDys
        global totalSmoothStore
        centerX = self.win.getXSize() / 2
        centerY = self.win.getYSize() / 2
        md = self.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if prevMouseVal == 0:
            prevMouseVal = 1
            prevDxs = []
            prevDys = []
        else:
            dx = x - prevMouseX
            dy = y - prevMouseY
            if len(prevDxs) > totalSmoothStore:
                prevDxs.pop(0)
            if len(prevDys) > totalSmoothStore:
                prevDys.pop(0)

            prevDxs.append(dx)
            prevDys.append(dy)

            curAverageDx = 0.
            for curDx in prevDxs:
                curAverageDx += curDx
            curAverageDx = curAverageDx / len(prevDxs)

            curAverageDy = 0.
            for curDy in prevDys:
                curAverageDy += curDy
            curAverageDy = curAverageDy / len(prevDys)
            self.camera.setP(self.camera.getP() -
                             5 * globalClock.getDt() * curAverageDy)
            self.camera.setH(self.camera.getH() -
                             5 * globalClock.getDt() * curAverageDx)

        prevMouseX = x
        prevMouseY = y
        return task.cont

    # Python code to convert string to list
    def str2list(self, string):
        li = list(map(int, list(string.split(","))))
        return li

    def loadmodels(self):
        # an earth model
        global Actors
        sql = 'select * from ' + table_name
        s = self.db.executeQuery(sql, '')
        st = []
        for st in s:
            Mem.createobject(mass=self.str2list(st[2]),
                             cor=self.str2list(st[6]),
                             vel=self.str2list(st[7]))
            tmp = self.loader.loadModel("res/tmp/earth/earth")
            tmp.reparentTo(self.render)
            pos = self.str2list(st[6])
            tmp.setPos(pos[0], pos[1], pos[2])
            # Actors.append(tmp)


app = stellarMovementSimulator()
app.run()
