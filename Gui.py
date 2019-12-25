'''
@Author: Alicespace
@Date: 2019-12-25 10:03:35
@LastEditTime : 2019-12-25 18:10:06
'''
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenGeom import OnscreenGeom
from direct.gui.DirectGui import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from panda3d.core import TransparencyAttrib
from Mem import createobject, reinitialize, objects
import Mem
import World
import sys, csv, os, random
import tkinter as tk
from tkinter import filedialog

leftframe = None
path = 'res/card/'
path0 = 'res/texture/gui-texture/'
# TODO where is slant?
#some mess and their explanation
timeRateBar = 1
tip = ''  #str object for checking whether to give tips or not
ftip, stip, ttip = 1, 2, 3  #tips
Filepath = None  #filepath to load texture(temporary)
f, bv = 0, 0  #arg to see if file is chosen(temporary)
initTextObject, StartButton = 1, 1  #Welcom direct
StarMenu, StarMenucanvas = 1, 1  #Main menu and its canvas to move
canvasSize = (0, 0.996, -1.3, 1)  #Initial StarMenu['frameSize']
entryList, entryErrorList = 1, [None for k in range(9)]  #While creating a card(temporary)
typeCard, typeframe = list(range(4)), list(range(4))  #4 types of stars
Del = []
MyStar=[]
Type = ['Eplanet', 'Jplanet', 'starO', 'starG']
triggerstate = False


class geneText(ShowBase):
    def __init__(self, parenT, texT, scalE, poS):
        self.text = OnscreenText(parent=parenT,
                                 text=texT,
                                 scale=scalE,
                                 pos=poS)


class geneFrame(ShowBase):
    def __init__(self, parenT, size, pos, color, relieF):
        self.frame = DirectFrame(parent=parenT,
                                 frameSize=size,
                                 pos=pos,
                                 frameColor=color,
                                 relief=relieF)


class geneEntry(ShowBase):
    def __init__(self, parenT, scalE, poS, widtH, relieF, commanD, extra):
        self.entry = DirectEntry(parent=parenT,
                                 scale=scalE,
                                 pos=poS,
                                 width=widtH,
                                 relief=relieF,
                                 command=commanD,
                                 extraArgs=extra)


def OpenMenu():
    global StarMenu, StarMenucanvas, timeRateBar
    global world
    try:
        world.takeMouseAway()
    except:
        pass
    StarMenu = DirectScrolledFrame(relief=0,
                                   frameSize=(0, 0.99, -1.1, 1),
                                   canvasSize=canvasSize,
                                   pos=(0.79, 0, 0),
                                   scrollBarWidth=0.04)

    StarMenucanvas = StarMenu.getCanvas()
    StarMenucanvasParent = StarMenucanvas.getParent()

    timeRateBar = DirectScrollBar(parent=StarMenu,
                                  value=20,
                                  range=(0, 80),
                                  pageSize=2,
                                  scrollSize=1,
                                  pos=(-1, 0, 0.92),
                                  frameSize=(-0.6, 0.6, -0.045, 0),
                                  frameColor=(0.2, 0.43, 0.88, 0.2),
                                  manageButtons=True,
                                  resizeThumb=True,
                                  command=guiChangeTimeRate,
                                  thumb_relief=1,
                                  thumb_frameTexture=path0 + 'pr.jpg',
                                  incButton_relief=1,
                                  incButton_frameTexture=path0 + 'timr.jpg',
                                  decButton_relief=1,
                                  decButton_frameTexture=path0 + 'timl.jpg')
    timeLabel = DirectLabel(
        parent=timeRateBar,
        text=
        '\1purp\1* Time Proportional Scale *\2\n|                |                |\n10^5           10^6            10^7           10^8           10^9',
        relief=0,
        scale=0.06,
        pos=(0, 0, 0.02))

    Species()
    Cut_off = geneFrame(StarMenucanvas, (0, 0.965, -0.02, 0), (0, 0, -0.073),
                        (0.5, 0.5, 0.5, 1), 2)
    cut_off = geneText(Cut_off.frame, '\1white\1.\2' * 42, 0.1,
                       (0.47, -0.011, 0))

    Ch_button = DirectButton(parent=StarMenucanvas,
                             frameTexture=path0 + 'timl.jpg',
                             relief=2,
                             scale=0.07,
                             pos=(0, 0, -0.8),
                             text='\1light\1Change\2',
                             command=ChButton)

    try:
        for star in MyStar:
            generateCard(star)
    except:
        pass
    print(MyStar)

    base.win.getEngine().renderFrame()
    # Only calling DSF.guiItem.recompute() gives imprecise position.
    # DSF.guiItem.recompute()
    StarMenucanvasDefaultPos = StarMenucanvas.getPos()

    # Must know the canvas position range
    StarMenu['horizontalScroll_value'] = StarMenu['verticalScroll_value'] = 1
    StarMenu.guiItem.recompute()
    StarMenucanvasRange = StarMenucanvasDefaultPos - StarMenucanvas.getPos()
    StarMenucanvasRange[0] = abs(StarMenucanvasRange[0])
    StarMenucanvasRange[2] = abs(StarMenucanvasRange[2])
    StarMenu['horizontalScroll_value'] = StarMenu['verticalScroll_value'] = 0

    def startScroll():
        m = base.mouseWatcherNode.getMouse()
        m = StarMenucanvasParent.getRelativePoint(render2d,
                                                  Point3(m[0], 0, m[1]))
        fs = StarMenu['frameSize']
        if fs[0] < m[0] < fs[1] and fs[2] < m[2] < fs[3]:
            task = taskMgr.add(scroll, 'scrolltask')
            task.startMouse = m
            task.canvasOrigPos = StarMenucanvas.getPos(
            ) - StarMenucanvasDefaultPos
            base.accept('mouse1-up', taskMgr.remove, [task])

    def scroll(task):
        m = base.mouseWatcherNode.getMouse()
        m = StarMenucanvasParent.getRelativePoint(render2d,
                                                  Point3(m[0], 0, m[1]))
        canvasPos = task.canvasOrigPos + (m - task.startMouse)
        StarMenu[
            'horizontalScroll_value'] = -canvasPos[0] / StarMenucanvasRange[0]
        StarMenu[
            'verticalScroll_value'] = canvasPos[2] / StarMenucanvasRange[2]
        return task.cont

    base.accept('mouse1', startScroll)
    keyRegMgr.regKeysInit()
    base.accept('q', hideMenu)


def CloseMenu():
    StarMenu.destroy()
    return None


def ChButton():
    global Ca, World
    World.end()
    update()
    Ca = 1
    StarMenu.destroy()
    OpenMenu()


def guiChangeTimeRate():
    global World
    rate = timeRateBar['value']
    rate = 10**int(rate / 20)
    World.changeTimeRate(rate)


def hideMenu():
    global StarMenu, World
    StarMenu.hide()
    World.takeMouseBack()
    base.accept('q', showMenu)

def showMenu():
    global StarMenu, World
    StarMenu.show()
    World.takeMouseAway()
    base.accept('q', hideMenu)


def Species():  #four basic cards to create object
    global typeCard, typeframe
    typeText = [
        '\1light\1Earth like Planet\2', '\1light\1Jupiter like planet\2',
        '\1light\1O-type Star\2', '\1light\1G-type Star\2'
    ]
    for i in range(4):
        typeframe[i] = DirectFrame(parent=StarMenucanvas,
                                   frameSize=(0, 0.955, -0.26, 0),
                                   pos=(0, 0, 1 - 0.27 * i),
                                   relief=1,
                                   frameTexture=path + '11' + str(i + 2) +
                                   '1.jpg',
                                   image_scale=0.25,
                                   text=typeText[i],
                                   text_pos=(0.75, -0.23, 0),
                                   text_scale=0.05)
        typeCard[i] = DirectCheckButton(
            parent=typeframe[i],
            relief=0,
            boxRelief=1,
            boxImage=starImgs[i],
            scale=0.128,
            pos=(0.264, 0, -0.13),
            command=createLeftFrame,
            extraArgs=[Type[i],True])  #i is the order of the type

def createLeftFrame(button, objtype, newStar, starNumber=None):
    global leftframe, entryList, entryErrorList, dataS, World, Filepath
    Tipmgr = TipMgr()
    Tipmgr.VariousTip()
    try:
        Filepath = MyStar[starNumber].texture
    except:
        Filepath = None
    if leftframe != None:
        leftframe.destroy()
    else:
        pass
    leftframe = DirectFrame(parent=StarMenu,
                            relief=1,
                            frameSize=(0, 0.8, -1, 1),
                            frameColor=(0.7, 0.7, 0.2, 1),
                            pos=(-2.58, 0, 0))
    leftframe['frameTexture'] = path + 'frameTexture' + '-' + objtype + '.jpg'
    entries = [
        'Name', 'mass\t\t   kg', 'radius\t\t   km', 'x\t\t\tkm', 'y\t\t\tkm',
        'z\t\t\tkm', 'v_x\t\t\tkm/s', 'v_y\t\t\tkm/s', 'v_z\t\t\tkm/s'
    ]
    entryList, textList = [], []

    def init(num):
        t = DirectEntry(parent=leftframe,
                        scale=0.063,
                        width=8,
                        relief=1,
                        pos=(0.1, 0, 0.8),
                        extraArgs=[num])
        entryList.append(t)
        t = OnscreenText(parent=entryList[num],
                         text=entries[num],
                         scale=0.7,
                         pos=(1.5, 1.5, 0),
                         fg=(0.5, 1, 0.9, 1))
        textList.append(t)
        return None

    def withArguments(num):
        t = DirectEntry(parent=leftframe,
                        scale=0.06,
                        width=5,
                        relief=1,
                        pos=(0.17, 0, 0.7 - 0.17 * num),
                        extraArgs=[num])
        entryList.append(t)
        t = OnscreenText(parent=entryList[num],
                         text=entries[num],
                         scale=0.7,
                         pos=(2, 0, 0),
                         fg=(0.5, 1, 0.9, 1))
        textList.append(t)
        return None

    def withoutArguments(num):
        t = DirectEntry(parent=leftframe,
                        scale=0.06,
                        width=7,
                        relief=1,
                        pos=(0.17, 0, 0.7 - 0.17 * num),
                        extraArgs=[num])
        entryList.append(t)
        t = OnscreenText(parent=entryList[num],
                         text=entries[num],
                         scale=0.7,
                         pos=(3.6, 0, 0),
                         fg=(0.5, 1, 0.9, 1))
        textList.append(t)
        return None

    for num in range(9):
        if num == 0:
            init(num)
        else:
            if num < 3:
                withArguments(num)
            else:
                withoutArguments(num)
    if newStar == False:
        star = MyStar[starNumber]
        dataS = [
            star.name, star.mass, star.radius, star.cor[0], star.cor[1],
            star.cor[2], star.vel[0], star.vel[1], star.vel[2]
        ]
        for num in range(9):
            entryList[num].enterText(str(dataS[num]))
    closeEntry = YesNoDialog(
        parent=leftframe,
        buttonValueList=[0, 1],
        buttonTextList=['\1blgr\1Close\2', '\1blgr\1Done\2'],
        button_relief=2,
        scale=0.8,
        pos=(0.56, 0, -0.75),
        relief=0,
        command=closeLeftFrame,
        extraArgs=[objtype, newStar, starNumber])
    textureSet = OkDialog(parent=leftframe,
                          buttonTextList=['\1pink\1Various\2'],
                          button_relief=2,
                          scale=0.8,
                          pos=(0.56, 0, -0.64),
                          relief=0,
                          command=chooseTexture)
    textureSet['button_frameTexture'] = leftframe['frameTexture']
    closeEntry['button_frameTexture'] = leftframe['frameTexture']
    base.ignore('q')
    base.ignore('r')

def chooseTexture(x):  #give a tk or list to choose texture
    global Filepath
    root = tk.Tk()
    root.withdraw()
    Filepath = filedialog.askopenfilename()  #获得选择好的文件
    return None

def closeLeftFrame(button, objtype, newStar, starNumber=None):
    global entryList, entryErrorList, leftframe, MyStar, canvasSize, StarMenu
    legitimate = True
    if button == 1:    #'Done'
        dataS = []
        dataS.append(entryList[0].get())
        for le in range(1, 9):
            dataS.append(entryList[le].get())
            acceptText = '\1roman\1\1green\1Change Accepted\2\2'
            rejectText = '\1roman\1\1red\1Change Rejected\2\2'
            try:
                dataS[le] = float(dataS[le])
                t = OnscreenText(parent=entryList[le],
                                 text=acceptText,
                                 scale=0.68,
                                 pos=(0.8, -1, 0))
                entryErrorList[le] = t
            except:
                t = OnscreenText(parent=entryList[le],
                                 text=rejectText,
                                 scale=0.68,
                                 pos=(0.8, -1, 0))
                entryErrorList[le] = t
                legitimate = False
        if legitimate:
            Mem.reinitialize()
            if newStar == False:
                if dataS[0] == None:
                    dataS[0] = 'Default Object'
                else:
                    pass
                n = starNumber
                MyStar[n].name, MyStar[n].mass, MyStar[n].radius,\
                MyStar[n].cor[0], MyStar[n].cor[1], MyStar[n].cor[2], \
                MyStar[n].vel[0], MyStar[n].vel[1], MyStar[n].vel[2],
                MyStar[n].texture = dataS + [Filepath]
            else:
                if dataS[0] == None:
                    dataS[0] = 'Default Object'
                else:
                    pass
                Mem.processcreate(objtype=objtype,
                              texture=Filepath,
                              myname=dataS[0],
                              mass=dataS[1],
                              radius=dataS[2],
                              vel=[dataS[6], dataS[7], dataS[8]],
                              cor=[dataS[3], dataS[4], dataS[5]])
                MyStar = Mem.getcurrentobjects()
                print(MyStar)
                canvasSize = (0, 0.996, StarMenu['canvasSize'][2] - 0.675, 1)
            leftframe.destroy()
            CloseMenu()
            OpenMenu()
        else:
            pass
    elif button == 0:    #"Close"
        leftframe.destroy()
        CloseMenu()
        OpenMenu()
    leftframe = None
    return None


def generateCard(obj):
    global velo, posi, underChangeState
    starNumber = MyStar.index(obj)
    openCount, closedCount = 0, 0
    info = '\1roman\1mass: %d   kg\nradius: %d   km\2' % (obj.mass, obj.rad)
    for obj in MyStar[0:starNumber]:
        if obj.switch == True:
            openCount = openCount + 1
        else:
            closedCount = closedCount + 1
    cardPosition = 0 - 0.093 - closedCount * 0.365 - openCount * 0.690
    card = DirectFrame(
        pos=(0, 0, cardPosition),
        frameTexture=path + 'frameTexture' + '-' + obj.objtype + '/.jpg',
        frameSize=(0.02, 0.95, -0.35, 0),
        #frameColor=(0.65 - starNumber * 0.13, 0.73 - starNumber * 0.08,
                    )#0.86 - starNumber * 0.13, 1))
    card.reparentTo(StarMenucanvas)
    myButton = DirectCheckButton(parent=card,
                                 boxRelief=1,
                                 boxBorder=0,
                                 boxImage=path + 'boxTexture' + '-' + objtype +
                                 '.jpg',
                                 scale=0.174,
                                 pos=(0.378, 0, -0.174),
                                 relief=0,
                                 command=Change,
                                 extraArgs=[starNumber])
    myInfo = OnscreenText(parent=card,
                          text=info,
                          mayChange=1,
                          align=TextNode.ACenter,
                          pos=(0.675, -0.2, 0),
                          scale=0.055,
                          fg=(0.7, 0.5, 1, 1))
    myName = OnscreenText(parent=myMass,
                          text=obj.name,
                          mayChange=1,
                          align=TextNode.ACenter,
                          pos=(0.675, -0.12, 0),
                          scale=0.058,
                          fg=(0.96, 0.97, 1, 1))
    if obj.switch == False:
        card = DirectFrame(parent=card,
                           frameTexture=card['frameTexture'],
                           frameSize=(0, 0.91, -0.32, 0),
                           frameColor=(0.6 - starNumber * 0.13,
                                       0.7 - starNumber * 0.08,
                                       0.8 - starNumber * 0.13, 1),
                           relief=1)
        card.setPos(0.025, 0, -0.35)
        velo[indexNum], posi[indexNum] = [], []
        vl = ['\1roman\1vx\2', '\1roman\1vy\2', '\1roman\1vz\2']
        ps = ['\1roman\1x\2', '\1roman\1y\2', '\1roman\1z\2']
        for i in range(3):
            velo[indexNum][i] = DirectEntry(
                parent=card,
                initialText='{:'
                '>8}'.format(int(v[i])) +
                '{:.3f}'.format(v[i] - int(v[i])[1:]),
                scale=.035,
                pos=(0.055 + i * 0.234, 0, -0.218),
                relief=1,
                width=5.2,
                extraArgs=[starNumber, 2, objtype])
            vl[i] = OnscreenText(parent=velo[starNumber][i],
                                 text=vl[i],
                                 scale=1.2,
                                 pos=(-0.9, 0, 0),
                                 fg=(0.5, 1, 0.9, 1))
        V = OnscreenText(parent=velo[starNumber][1],
                         text='\1roman\1Velocity\2',
                         scale=1.2,
                         pos=(2.5, 1.7, 0),
                         align=TextNode.ACenter,
                         fg=(0.9, 0.85, 0.14, 1))
        UnV = OnscreenText(parent=velo[starNumber][2],
                           text='\1roman\1\1blgr\1km/s\2\2',
                           scale=1.2,
                           pos=(6.7, 0, 0))
        for j in range(3):
            posi[starNumber][2 - j] = DirectEntry(
                parent=card,
                initialText='{:'
                '>8}'.format(int(p[i])) +
                '{:.3f}'.format(p[i] - int(p[i])[1:]),
                scale=.035,
                pos=(0.055 + (2 - j) * 0.234, 0, -0.11),
                relief=1,
                width=5.2,
                extraArgs=[n, 1, j])
            ps[2 - j] = OnscreenText(parent=posi[starNumber][2 - j],
                                     text=ps[2 - j],
                                     scale=1.2,
                                     pos=(-0.9, 0, 0),
                                     fg=(0.5, 1, 0.9, 1))
        P = OnscreenText(parent=posi[starNumber][1],
                         text='\1roman\1Position\2',
                         scale=1.2,
                         pos=(2.5, 1.7, 0),
                         align=TextNode.ACenter,
                         fg=(0.9, 0.14, 0.85, 1))
        UnP = OnscreenText(parent=posi[starNumber][2],
                           text='\1roman\1\1blgr\1km\2\2',
                           scale=1.2,
                           pos=(6.7, 0, 0))
        if underChangeState == True:
            myTr = YesNoCancelDialog(parent=card,
                                     relief=0,
                                     scale=0.62,
                                     button_relief=0,
                                     buttonTextList=[
                                         '\1blgr\1Close\2',
                                         '\1blgr\1Change Args\2',
                                         '\1blgr\1Delete\2'
                                     ],
                                     button_scale=1.1,
                                     pos=(0.5, 0, -0.186),
                                     buttonValueList=[-1, 0, 1],
                                     command=closeChange,
                                     extraArgs=[starNumber])
        else:
            myTr = OkDialog(parent=card,
                            relief=0,
                            scale=0.62,
                            button_relief=0,
                            buttonTextList=['\1blgr\1Close\2'],
                            buttonValueList=[-1],
                            button_scale=1.1,
                            pos=(0.67, 0, -0.186),
                            command=closeChange,
                            extraArgs=[starNumber])
    else:
        pass

    return None


def Change(x, y):
    global StarMenu, MyStar
    MyStar[y].switch = -1
    CloseMenu()
    OpenMenu()


def closeChange(x,starNumber):
    global StarMenu,MyStar,Del
    if x==-1:
        MyStar[starNumber].switch=None
        CloseMenu()
        OpenMenu()
    elif x==0:
        createLeftFrame(button = True, objtype = MyStar[starNumber].objtype,
                        newStar = False, starNumber = starNumber)
    else:
        Mem.reinitialize()
        Mem.processdelete([MyStar[starNumber]])
        MyStar.pop(starNumber)
        CloseMenu()
        OpenMenu()


def update():
    global velo, posi
    if not triggerstate:
        for y in range(len(MyStar)):
            if MyStar[y].switch == -1:
                for i in range(3):
                    posi[y][i].enterText('{:' '>8}'.format(int(MyStar[y].cor[i])) +\
                         '{:.3f}'.format(MyStar[y].cor[i] -int(MyStar[y].cor[i])))
                    velo[y][i].enterText('{:' '>8}'.format(int(MyStar[y].vel[i])) +\
                         '{:.3f}'.format(MyStar[y].vel[i] -int(MyStar[y].vel[i])))
            else:
                pass
    else:
        MyStar = Mem.getcurrentobjects()
        CloseMenu()
        OpenMenu()



class worldSwitch:
    def __init__(self):
        global World
        self.switchStatus = False

    def switch(self):
        if self.switchStatus is False:
            base.taskMgr.add(World.start, 'start')
            self.switchStatus = True
        elif self.switchStatus is True:
            World.end()
            self.switchStatus = False


class guiRenderReg:
    def __init__(self):
        self.tp = TextPropertiesManager.getGlobalPtr()
        self.setWordStyle()
        self.setCardStyle()

    def setWordStyle(self):
        try:
            self.fg('purp', 0.8, 0.57, 0.95, 3.4)
            self.fg('gray', 0.76, 0.75, 0.77, 1)
            self.fg('pink', 0.86, 0.25, 0.6, 1)
            self.fg('light', 0.8, 1, 0.5, 2)
            self.fg('blgr', 0.5, 1, 0.9, 1.4)
            self.fg('green', 0, 0.4, 1, 1.5)
            self.fg('blue', 0.3, 0.5, 0.65, 1)
            self.fg('blood', 0.83, 0.39, 0.44, 2)
            self.fg('red', 1, 0.2, 0, 2)
            self.fg('white', 1, 1, 1, 1)
            self.setfont('cmtt12', 'roman')
            # TODO no such font
        except:
            pass

    def setCardStyle(self):
        global starImgs
        starImgs = []
        starImgPath = getPath() + '/res/card/starImg/'
        starImgs.append(base.loader.loadTexture(starImgPath + 'Eplanet.jpg'))
        starImgs.append(base.loader.loadTexture(starImgPath + 'Jplanet.jpg'))
        starImgs.append(base.loader.loadTexture(starImgPath + 'starO.jpg'))
        starImgs.append(base.loader.loadTexture(starImgPath + 'starG.jpg'))

    def setfont(self, filepath, name):
        self.font = base.loader.loadFont(filepath)
        tpF = TextProperties()
        tpF.setFont(self.font)
        self.tp.setProperties(name, tpF)

    def fg(self, name, r, g, b, a):
        tpG = TextProperties()
        tpG.setTextColor(r, g, b, a)
        self.tp.setProperties(name, tpG)


def getPath():
    '''
        绝对路径获取  
        '''
    path = os.path.abspath(sys.path[0])
    return Filename.fromOsSpecific(path).getFullpath()


class keyRegMgr:
    def regKeysInit():
        global WordSwitch
        WordSwitch = worldSwitch()
        base.accept('r', WordSwitch.switch)
        base.accept('control-e', sys.exit)

    def unregkeys():
        base.ignore('q')
        base.ignore('r')


class TipMgr:
    def __init__(self):
        self.statusDict = {}
        self.readcsv()

    def readcsv(self):
        csvPath = Filename(getPath() + '/res/config/Tips').toOsSpecific()
        if os.path.exists(csvPath):
            with open(csvPath, 'r') as tips:
                line = tips.readline()
                self.statusDict = eval(line)
        else:
            self.writecsv('NoTip', '0')
            self.writecsv('NoVtip', '0')

            self.readcsv()

    def writecsv(self, key, value):
        self.statusDict[key] = value
        csvPath = Filename(getPath() + '/res/config/Tips').toOsSpecific()
        with open(csvPath, 'w') as tips:
            tips.write(str(self.statusDict))

    def moveTip(self):
        if self.statusDict['NoTip'] == '0':
            movetipcontext = 'Use \'wasd\' to move, drag mouse to look around.\n\nChoose a card and click it to define your star.'
            self.movetip = YesNoDialog(text=movetipcontext,
                                       scale=1,
                                       pos=(-0.02, 0, 0.22),
                                       buttonTextList=['No tips', '\tNext'],
                                       buttonValueList=[0, 1],
                                       midPad=0.17,
                                       button_relief=0,
                                       relief=1,
                                       command=self.controlTip)

    def controlTip(self, lastchose):
        if self.movetip:
            self.movetip.destroy()
        if lastchose:
            pass
        else:
            self.writecsv('NoTip', '1')
        controlTipContext = 'Press \"R\" to run\n\n  Press \"Q\" to hide the Menu\n\n    Press \"ctrl+e\" to exit'
        self.controltip = YesNoCancelDialog(
            text=controlTipContext,
            scale=1,
            pos=(-0.02, 0, 0.22),
            buttonTextList=['No tips', '\tNext'],
            buttonValueList=[0, 1],
            midPad=0.1,
            button_relief=0,
            relief=1,
            command=self.endControlTip)

    def endControlTip(self, lastchose):
        self.controltip.destroy()
        if lastchose == 0:
            self.writecsv('NoTip', '1')

    def VariousTip(self):
        if self.statusDict['NoVtip'] == '1':
            return
        else:
            t_k3 = 'You can click \1pink\1\"Various\"\2 to design you own star!!!\n\nAnd notice English input is acceptable'
            self.Varioustip = YesNoDialog(text=t_k3,
                                        scale=1,
                                        pos=(-0.02, 0, 0.22),
                                        buttonTextList=['No tips', '\tClose'],
                                        buttonValueList=[0, 1],
                                        midPad=0.15,
                                        button_relief=0,
                                        relief=1,
                                        command=self.endVariousTip)

    def endVariousTip(self, lastchose):
        if lastchose == 1:
            pass
        else:
            self.writecsv('NoVtip', '1')
        self.Varioustip.destroy()


class gui(ShowBase):
    def __init__(self):
        self.setup()
        guiRenderReg()
        keyRegMgr.regKeysInit()
        self.welcome()

    def init(self):
        global World
        global initTextObject, StartButton
        World = World.world()
        initTextObject.destroy()
        StartButton.destroy()
        Tipmgr = TipMgr()
        Tipmgr.moveTip()
        OpenMenu()

    def setup(self):
        loadPrcFileData('', 'fullscreen false')
        wp = WindowProperties()
        wp.setSize(1920, 1080)
        base.win.requestProperties(wp)

    def welcome(self):
        global initTextObject, StartButton
        welcomeText = '\1roman\1\1slant\1Hello! Welcome to our\n\1blood\1Stellar Movement Simulator\2\2\n \1slant\1Hope you enjoy yourself\2'
        initTextObject = OnscreenText(text=welcomeText,
                                      pos=(0.0, 0.25),
                                      fg=(0.5, 0.7, 0.8, 1),
                                      scale=0.1,
                                      align=TextNode.ACenter,
                                      mayChange=0)
        StartButton = DirectButton(text=("Click", "\1blue\1G O O D !\2",
                                         "Yes,it\'s here"),
                                   pos=(0, 0, -.25),
                                   scale=.07,
                                   relief=0,
                                   command=self.init)
