'''

## 用来生成3D世界  

@Author: Alicespace  
@Date: 2019-11-18 08:06:30  
@LastEditTime : 2019-12-26 02:09:52

'''

import calculateloop, Mem, starGui
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.interval.LerpInterval import LerpPosInterval
from panda3d.core import CollisionHandlerQueue, CollisionHandlerEvent, CollisionTraverser, CollisionSphere, CollisionNode, CollisionHandlerPusher, TransparencyAttrib, TextNode, PointLight, loadPrcFile, Point3, loadPrcFileData, WindowProperties, Texture, TextureStage, DirectionalLight, AmbientLight, VBase4, TexGenAttrib
from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename
from direct.task import Task
from direct.actor import Actor
import os, sys, random
table_name = 'Star_info'
global time_rate
time_rate = 0.01
Actors = {}
Sequences = {}
ObjOrder = 0
ActorsOn = [False for i in range(105)]
global pos_rate
pos_rate = 1.5


class cameraSpeed():
    '''
    摄像机速度控制类
    '''
    def __init__(self):
        self.defaultMoveSpeed = 10
        self.minVelocity = 0.001
        self.velocityDecayRate = 0.5
        self.Vx = 0
        self.Vy = 0
        self.Vz = 0

    def addVx(self, dt):
        '''
        更改x速度
        '''
        self.Vx += self.defaultMoveSpeed * dt

    def addVy(self, dt):
        '''
        更改y速度
        '''
        self.Vy += self.defaultMoveSpeed * dt

    def addVz(self, dt):
        '''
        更改z速度
        '''
        self.Vz += self.defaultMoveSpeed * dt

    def slideX(self):
        '''
        x方向滑动动画
        '''
        if (abs(self.Vx) <= self.minVelocity):
            self.Vx = 0
        if (self.Vx != 0):
            self.Vx *= self.velocityDecayRate

    def slideY(self):
        '''
        y方向滑动动画
        '''
        if (abs(self.Vy) <= self.minVelocity):
            self.Vy = 0
        if (self.Vy != 0):
            self.Vy *= self.velocityDecayRate

    def slideZ(self):
        '''
        z方向滑动动画
        '''
        if (abs(self.Vz) <= self.minVelocity):
            self.Vz = 0
        if (self.Vz != 0):
            self.Vz *= self.velocityDecayRate


class world(ShowBase):
    ''' 
    3D世界基类  
    '''
    def __init__(self):
        self.collisionHandler()
        self.setup()
        self.setCameraSpinConst()
        self.regKey()
        self.setTasks()
        self.cameraCollision()
        self.setSky()

    def getPath(self):
        '''
        绝对路径获取  
        '''
        path = os.path.abspath(sys.path[0])
        self.currentDIR = Filename.fromOsSpecific(path).getFullpath()

    def setCameraSpinConst(self):
        '''
        设置摄像机旋转初始值
        '''
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

    def setup(self):
        '''
        窗口初始设定  
        常量初始化  
        '''
        base.disableMouse()
        # 鼠标放在中间
        global isEnded
        isEnded = False

        global CountUpdateGui
        CountUpdateGui = 0

        base.win.movePointer(0, int(base.win.getXSize() / 2),
                             int(base.win.getYSize() / 2))
        self.cameraSpeed = cameraSpeed()
        self.getPath()

    def cameraCollision(self):
        '''
        注册摄像机与星体表面的碰撞处理函数  
        '''
        base.cTrav = CollisionTraverser()
        pusher = CollisionHandlerPusher()
        fromObject = base.camera.attachNewNode(CollisionNode('cameracol'))
        fromObject.node().addSolid(CollisionSphere(0, 0, 0, 5))
        pusher = CollisionHandlerPusher()
        pusher.addCollider(fromObject, base.camera, base.drive.node())
        base.cTrav.addCollider(fromObject, pusher)

    def takeMouseAway(self):
        '''
        用于与GUI交互时释放焦点，卸载世界刷新任务  
        '''
        try:
            self.spinCameraTask.remove()
        except:
            pass
        props = WindowProperties()
        props.setCursorHidden(False)
        props.setMouseMode(WindowProperties.M_absolute)
        base.win.requestProperties(props)

    def start(self, task):
        """
        启动3D世界
        """
        global isEnded
        if isEnded:
            if self.startTask:
                pass
            else:
                self.startTask = base.taskMgr.doMethodLater(
                    0.1, self.start, 'start')
        else:
            self.loadmodelsinit()
            self.calculateStarTask = base.taskMgr.add(self.calculateStar,
                                                    'calculateStar')
            self.detectOrdTask = base.taskMgr.add(self.detectOrd, 'detectOrd')
            starGui.changeStarttingStatusout()

    def end(self):
        '''
        结束绘制世界
        '''
        global isEnded
        isEnded = True

    def takeMouseBack(self):
        '''
        用于与GUI交互时获取焦点，加载世界刷新任务
        '''
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        base.win.requestProperties(props)
        self.setCameraSpinConst()
        self.spinCameraTask = base.taskMgr.add(self.spinCamera, "spinCamera")

    def setTasks(self):
        '''
        添加控制任务  
        1. 摄像机移动  
        2. 天空球移动   
        '''
        base.taskMgr.add(self.moveCamera, "moveCamera")
        base.taskMgr.add(self.skysphereTask, "SkySphere Task")

    def collisionHandler(self):
        '''
        注册星体相互碰撞的事件处理函数
        '''
        self.collHandEvent = CollisionHandlerEvent()
        self.collHandEvent.addInPattern('%fn-into-%in')
        self.accept('starscol-into-starscol', self.handleStarCollision)

    def handleStarCollision(self, entry):
        '''
        星体碰撞的粒子效果
        
        .. todo::
                视觉效果不明显，换一个？
        '''
        base.enableParticles()
        p = ParticleEffect()
        p.loadConfig(self.currentDIR + '/res/particles/dust.ptf')
        p.start(parent=base.render, renderParent=base.render)
        p.setPos(entry.getSurfacePoint(base.render))
        p.setScale(1000000)

    def regKey(self):
        '''
        注册按键响应事件
        '''
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

    def setSky(self):
        '''
        加载天空球
        '''
        # load sky sphere
        self.skysphere = base.loader.loadModel(self.currentDIR +
                                               "/res/skyBg/InvertedSphere.egg")
        self.skysphere.setTexGen(TextureStage.getDefault(),
                                 TexGenAttrib.MWorldPosition)
        self.skysphere.setTexProjector(TextureStage.getDefault(), base.render,
                                       self.skysphere)
        self.skysphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.skysphere.setTexScale(TextureStage.getDefault(), .5)
        tex = base.loader.loadCubeMap(self.currentDIR +
                                      "/res/skyBg/BlueGreenNebula__#.png")
        self.skysphere.setTexture(tex)
        self.skysphere.setLightOff()
        self.skysphere.setScale(10000)
        self.skysphere.reparentTo(base.render)
        self.skysphere.setBin('background', 1)
        self.skysphere.setDepthWrite(0)
        self.skysphere.reparentTo(base.render)

    def skysphereTask(self, task):
        '''
        移动天空球
        '''
        self.skysphere.setPos(base.camera, 0, 0, 0)
        return task.cont

    # Records thse state of the arrow keys
    def setKey(self, key, value):
        '''
        注册按键函数
        '''
        self.keyMap[key] = value

    # Define a procedure to move the camera.
    def moveCamera(self, task):
        '''
        注册```Panda```任务来移动摄像机
        '''
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
        if not isXMoved:
            self.cameraSpeed.slideX()
        if not isYMoved:
            self.cameraSpeed.slideY()
        base.camera.setX(base.camera, self.cameraSpeed.Vx * 0.5)
        base.camera.setY(base.camera, self.cameraSpeed.Vy)
        return task.cont

    def spinCamera(self, task):
        '''
        注册```Panda```任务来旋转摄像机
        '''
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
        '''
        检测`Mem.riggerstate`，判断是否发生融合事件
        '''
        global objs
        global ObjOrder, isEnded
        if isEnded:
            isEnded = False
            self.calculateStarTask.remove()
            return task.done
        else:
            if Mem.triggerstate is True:
                starGui.triggerstate = True
                Mem.triggerstate = False
                self.loadmodelsinit()
                return task.cont
            else:
                for obj in objs:
                    self.refreshSequence(obj)
                self.updategui()
                return task.cont

    def updategui(self):
        '''
        按照时间更新GUI数据
        '''
        global CountUpdateGui
        if CountUpdateGui > 30:
            CountUpdateGui = 0
            starGui.update()
        else:
            CountUpdateGui += 1

    def refreshSequence(self, obj):
        '''
        更新```Panda```序列，用于控制形体的运动
        '''
        global Sequences, pos_rate, time_rate
        if Sequences[obj.ID][0].isStopped() and ActorsOn[obj.ID] is True:
            Sequences[obj.ID] = Sequence()
            data = obj.dataOUT()
            Sequences[obj.ID].append(Actors[obj.ID].posInterval(
                data[0] * time_rate,
                Point3(data[4] * pos_rate, data[5] * pos_rate,
                       data[6] * pos_rate)))
            Sequences[obj.ID].start()

    def calculateStar(self, task):
        '''
        注册```Panda```任务，调用```calculate```进行计算
        '''
        calculateloop.loopjudge(length=1000)
        return task.cont

    def changeTimeRate(self, newRate):
        '''
        GUI调整时间比例的接口函数
        '''
        global time_rate
        time_rate = newRate

    def loadmodelsinit(self):
        '''
        初始化世界，加载星体模型，创建恒星粒子效果
        '''
        calculateloop.loopjudge(length=1000)
        global objs
        global Actors
        global ActorsOn
        global pos_rate
        global time_rate
        global Actors
        global ActorsOn
        global Sequences
        for obj in Actors:
            Actors[obj].removeNode()
        Actors = {}
        ActorsOn = [False for i in range(105)]
        Sequences = {}
        objs = Mem.getcurrentobjects()
        for obj in objs:
            data = obj.dataOUT()
            ActorsOn[obj.ID] = True
            Actors[obj.ID] = base.loader.loadModel(
                self.currentDIR + '/res/sphereTemplate/smiley.egg')
            tex = base.loader.loadTexture(
                self.seleceTexture(obj.objtype, obj.texture))
            Actors[obj.ID].setTexture(tex, 1)

            # Reparent the model to render.
            Actors[obj.ID].reparentTo(base.render)
            # Apply scale and position transforms on the model.

            Actors[obj.ID].setPos(data[4] * pos_rate, data[5] * pos_rate,
                                  data[6] * pos_rate)

            fromObject = Actors[obj.ID].attachNewNode(
                CollisionNode('starscol'))
            fromObject.node().addSolid(CollisionSphere(0, 0, 0, 1.15))
            Actors[obj.ID].setScale(obj.radius * pos_rate)
            base.cTrav.addCollider(fromObject, self.collHandEvent)
            if obj.objtype == 'starO' or obj.objtype == 'starG':
                base.enableParticles()
                p = ParticleEffect()
                p.loadConfig(self.currentDIR + '/res/particles/dust.ptf')
                p.start(parent=Actors[obj.ID], renderParent=Actors[obj.ID])
        if Mem.triggerstate is True:
            Mem.triggerstate = False
            return self.loadmodelsinit()
        else:
            for obj in objs:
                Sequences[obj.ID] = Sequence()
                data = obj.dataOUT()
                Sequences[obj.ID].append(Actors[obj.ID].posInterval(
                    data[0] * time_rate,
                    Point3(data[4] * pos_rate, data[5] * pos_rate,
                           data[6] * pos_rate)))
                Sequences[obj.ID].start()

    def seleceTexture(self, objtype, texture):
        if not texture:
            if objtype == 'starO':
                return self.selectRandomFile(self.currentDIR +
                                             '/res/texture/starO/')
            elif objtype == 'starG':
                return self.selectRandomFile(self.currentDIR +
                                             '/res/texture/starG/')
            elif objtype == 'Jplanet':
                return self.selectRandomFile(self.currentDIR +
                                             '/res/texture/Jplanet/')
            elif objtype == 'Eplanet':
                return self.selectRandomFile(self.currentDIR +
                                             '/res/texture/Eplanet/')
        else:
            return texture

    def selectRandomFile(self, fileDir):
        pt = Filename(fileDir).toOsSpecific()
        pathDir = os.listdir(pt)
        selectedPic = random.sample(pathDir, 1)
        fileselected = Filename.fromOsSpecific(os.path.join(
            pt, selectedPic[0])).getFullpath()
        return fileselected
