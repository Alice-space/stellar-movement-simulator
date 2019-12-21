'''
@Author: Alicespace
@Date: 2019-11-18 08:06:30
@LastEditTime : 2019-12-21 16:28:08
'''

import sys
from calculate import calculateloop
from calculate import Mem
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.interval.LerpInterval import LerpPosInterval
from panda3d.core import CollisionTraverser, CollisionSphere, CollisionNode, CollisionHandlerPusher, TransparencyAttrib, TextNode, PointLight, loadPrcFile, Point3, loadPrcFileData, WindowProperties, Texture, TextureStage, DirectionalLight, AmbientLight, VBase4, TexGenAttrib

from direct.showbase.ShowBase import ShowBase

from direct.task import Task
from direct.actor import Actor

# from pandac.PandaModules import WindowProperties, Texture, TextureStage, DirectionalLight, AmbientLight, TexGenAttrib
table_name = 'Star_info'
time_rate = 3
Actors = {}
Sequences = {}
ObjOrder = 0
ActorsOn = [False for i in range(105)]
global pos_rate
pos_rate = 10


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


class world(ShowBase):
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
        self.test()
        self.setup()
        self.regKey()
        self.setConst()
        self.setTasks()
        self.cameraCollision()
        self.setSky()

    def setup(self):
        # some properties about window and mouse
        base.disableMouse()
        base.win.movePointer(0, int(base.win.getXSize() / 2),
                             int(base.win.getYSize() / 2))
        # instance a speed object
        self.cameraSpeed = cameraSpeed()

    def cameraCollision(self):
        base.cTrav = CollisionTraverser()
        pusher = CollisionHandlerPusher()
        fromObject = base.camera.attachNewNode(CollisionNode('colNode'))
        fromObject.node().addSolid(CollisionSphere(0, 0, 0, 5))
        pusher = CollisionHandlerPusher()
        pusher.addCollider(fromObject, base.camera, base.drive.node())
        base.cTrav.addCollider(fromObject, pusher)

    def takeMouseAway(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        props.setMouseMode(WindowProperties.M_absolute)
        base.win.requestProperties(props)
        try:
            self.detectOrdTask.remove()
            self.calculateStarTask.remove()
        except:
            pass

    def takeMouseBack(self):
        props = WindowProperties()
        base.win.movePointer(0, int(base.win.getXSize() / 2),
                             int(base.win.getYSize() / 2))
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        base.win.requestProperties(props)
        self.detectOrdTask = base.taskMgr.add(self.detectOrd, "freshMove")
        self.calculateStarTask = base.taskMgr.doMethodLater(
            2, self.calculateStar, 'calculateStar')
        self.refreshActors()

    def setTasks(self):
        # add camera move task
        base.taskMgr.add(self.moveCamera, "moveCamera")
        base.taskMgr.add(self.skysphereTask, "SkySphere Task")
        base.taskMgr.add(self.spinCamera, "spinCamera")

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
        self.skysphere = base.loader.loadModel("res/skyBg/InvertedSphere.egg")
        self.skysphere.setTexGen(TextureStage.getDefault(),
                                 TexGenAttrib.MWorldPosition)
        self.skysphere.setTexProjector(TextureStage.getDefault(), base.render,
                                       self.skysphere)
        self.skysphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.skysphere.setTexScale(TextureStage.getDefault(), .5)
        tex = base.loader.loadCubeMap("res/skyBg/BlueGreenNebula__#.png")
        self.skysphere.setTexture(tex)
        self.skysphere.setLightOff()
        self.skysphere.setScale(10000)
        self.skysphere.reparentTo(base.render)
        self.skysphere.setBin('background', 1)
        self.skysphere.setDepthWrite(0)
        self.skysphere.reparentTo(base.render)

    def quitMain(self):
        sys.exit()

    def skysphereTask(self, task):
        self.skysphere.setPos(base.camera, 0, 0, 0)
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
        base.camera.setX(base.camera, self.cameraSpeed.Vx * 0.5)
        base.camera.setY(base.camera, self.cameraSpeed.Vy)
        return task.cont

    def spinCamera(self, task):
        global prevMouseX
        global prevMouseY
        global prevMouseVal
        global prevDxs
        global prevDys
        global totalSmoothStore
        centerX = base.win.getXSize() / 2
        centerY = base.win.getYSize() / 2
        md = base.win.getPointer(0)
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
            base.camera.setP(base.camera.getP() -
                             5 * globalClock.getDt() * curAverageDy)
            base.camera.setH(base.camera.getH() +
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
        global Sequences, pos_rate
        if Sequences[obj.ID][0].isStopped() and ActorsOn[obj.ID] is True:
            Sequences[obj.ID] = Sequence()
            data = obj.dataOUT()
            Sequences[obj.ID].append(Actors[obj.ID].posInterval(
                data[0] * time_rate,
                Point3(data[4] * pos_rate, data[5] * pos_rate,
                       data[6] * pos_rate)))
            Sequences[obj.ID].start()

    def calculateStar(self, task):
        calculateloop.loopjudge(length=1200)
        # task.delayTime += 1
        return task.again

    def loadmodelsinit(self):
        calculateloop.loopjudge(length=1200)
        global objs
        global Actors
        global ActorsOn
        global pos_rate
        objs = Mem.getcurrentobjects()
        for obj in objs:

            data = obj.dataOUT()
            ActorsOn[obj.ID] = True
            Actors[obj.ID] = base.loader.loadModel(obj.texture)
            # Reparent the model to render.
            Actors[obj.ID].reparentTo(base.render)
            # Apply scale and position transforms on the model.

            Actors[obj.ID].setPos(data[4] * pos_rate, data[5] * pos_rate,
                                  data[6] * pos_rate)

            fromObject = Actors[obj.ID].attachNewNode(CollisionNode('colNode'))
            fromObject.node().addSolid(CollisionSphere(0, 0, 0, 5))
            Actors[obj.ID].setScale(obj.radius * pos_rate)
            pusher = CollisionHandlerPusher()
            pusher.addCollider(fromObject, Actors[obj.ID])
            # base.cTrav.addCollider(fromObject, pusher)
        global Sequences
        for obj in objs:
            Sequences[obj.ID] = Sequence()
            data = obj.dataOUT()
            Sequences[obj.ID].append(Actors[obj.ID].posInterval(
                data[0] * time_rate,
                Point3(data[4] * pos_rate, data[5] * pos_rate,
                       data[6] * pos_rate)))
            Sequences[obj.ID].start()

    def test(self):
        Mem.createobject(objtype="star",
                         texture="res/tmp/earth/earth.egg",
                         mass=20,
                         radius=20,
                         cor=[150, 0, 0],
                         vel=[0, -11, 0])
        Mem.createobject(objtype="star",
                         texture="res/tmp/earth/earth.egg",
                         mass=30,
                         radius=30,
                         cor=[210, 340, 0],
                         vel=[0, -10, 0])

        calculateloop.loopjudge(length=120)
        global objs
        objs = Mem.getcurrentobjects()