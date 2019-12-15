'''
@Author: Alicespace
@Date: 2019-11-18 08:06:30
@LastEditTime: 2019-12-15 18:12:48
'''

import sys
from starDB import starDBManger
from calculate import calculateloop
from calculate import Mem
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.interval.LerpInterval import LerpPosInterval
from panda3d.core import PointLight, loadPrcFile, Point3, loadPrcFileData, WindowProperties, Texture, TextureStage, DirectionalLight, AmbientLight, VBase4, TexGenAttrib
from direct.actor.Actor import Actor
from direct.task import Task
# from pandac.PandaModules import WindowProperties, Texture, TextureStage, DirectionalLight, AmbientLight, TexGenAttrib
table_name = 'Star_info'
time_rate = 10
Actors = {}
Sequences = {}
ObjOrder = 0
ActorsOn = [False for i in range(105)]


def str2list(string):
    # Python code to convert string to list
    li = list(map(int, list(string.split(","))))
    return li


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
        self.test()
        self.setup()
        self.regKey()
        self.setConst()
        self.setTasks()
        self.setSky()
        self.loadmodelsinit()

    def setup(self):
        # some properties about window and mouse
        self.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        self.base.win.requestProperties(props)
        '''        # db
        self.db = starDBManger.DBTool(table_name)
        '''
        # instance a speed object
        self.cameraSpeed = cameraSpeed()

    def setTasks(self):
        # add camera move task
        self.taskMgr.add(self.moveCamera, "moveCamera")
        self.taskMgr.add(self.skysphereTask, "SkySphere Task")
        self.taskMgr.add(self.spinCamera, "spinCamera")
        self.taskMgr.add(self.detectOrd, "freshMove")
        self.taskMgr.doMethodLater(2, self.calculateStar, 'calculateStar')

    def regKey(self):
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

    def setConst(self):
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

    def setSky(self):
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

    def quitMain(self):
        # self.db.close()
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

    def detectOrd(self, task):
        global objs
        global ObjOrder
        if Mem.triggerstate is False:
            for obj in objs:
                if ObjOrder != obj.order:
                    self.refreshActors()
                    ObjOrder = obj.order
                    return task.cont
                elif ObjOrder == obj.order:
                    self.refreshSequence(obj)
            return task.cont
        else:
            Mem.triggerstate = False
            objs = Mem.getcurrentobjects()
            return task.cont

    def refreshActors(self):
        global Actors
        global ActorsOn
        global Sequences
        for obj in Actors:
            Actors[obj].removeNode()
        Actors = {}
        ActorsOn = [False for i in range(105)]
        Sequences = {}
        self.loadmodelsinit()

    def refreshSequence(self, obj):
        global Sequences
        if Sequences[obj.ID][0].isStopped() and ActorsOn[obj.ID] is True:
            Sequences[obj.ID] = Sequence()
            data = obj.dataOUT()
            Sequences[obj.ID].append(
                Parallel(
                    Actors[obj.ID].hprInterval(
                        data[0] * time_rate,
                        Point3(data[0] * time_rate, 0, 0),
                    ), Actors[obj.ID].posInterval(
                        data[0] * time_rate, Point3(data[4], data[5],
                                                    data[6]))))
            Sequences[obj.ID].start()

    def calculateStar(self, task):
        calculateloop.loopjudge(length=1200)
        # task.delayTime += 1
        return task.again

    def test(self):
        Mem.createobject(objtype="Eplanet",
                         texture="res/tmp/earth/earth.egg",
                         mass=10,
                         radius=30,
                         cor=[-5000, 0, 0],
                         vel=[0, -6000, 0])
        Mem.createobject(objtype="Eplanet",
                         texture="res/tmp/earth/earth.egg",
                         mass=10,
                         radius=10,
                         cor=[10000, 0, 0],
                         vel=[0, 7000, 0])
        Mem.createobject(objtype="star",
                         texture="res/tmp/earth/earth.egg",
                         mass=200,
                         radius=30,
                         cor=[-3000, 0, 0],
                         vel=[0, 11000, 0])
        Mem.createobject(objtype="star",
                         texture="res/tmp/earth/earth.egg",
                         mass=200,
                         radius=20,
                         cor=[1500, 0, 0],
                         vel=[0, -11000, 0])
        Mem.createobject(objtype="star",
                         texture="res/tmp/earth/earth.egg",
                         mass=300,
                         radius=30,
                         cor=[21, 34, 0],
                         vel=[0, -10, 0])

        calculateloop.loopjudge(length=120)
        global objs
        objs = Mem.getcurrentobjects()

    def loadmodelsinit(self):
        calculateloop.loopjudge(length=1200)
        global objs
        global Actors
        global ActorsOn
        objs = Mem.getcurrentobjects()
        for obj in objs:
            data = obj.dataOUT()
            ActorsOn[obj.ID] = True
            Actors[obj.ID] = self.loader.loadModel(obj.texture)
            # Reparent the model to render.
            Actors[obj.ID].reparentTo(self.render)
            # Apply scale and position transforms on the model.
            Actors[obj.ID].setPos(data[4], data[5], data[6])
            Actors[obj.ID].setScale(obj.radius)
        global Sequences
        for obj in objs:
            Sequences[obj.ID] = Sequence()
            data = obj.dataOUT()
            Sequences[obj.ID].append(
                Parallel(
                    Actors[obj.ID].hprInterval(
                        data[0] * time_rate,
                        Point3(data[0] * time_rate, 0, 0),
                    ), Actors[obj.ID].posInterval(
                        data[0] * time_rate, Point3(data[4], data[5],
                                                    data[6]))))
            Sequences[obj.ID].start()


app = stellarMovementSimulator()
app.run()
