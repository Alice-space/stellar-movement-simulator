'''
@Author: Alicespace
@Date: 2019-12-25 10:03:35
@LastEditTime : 2019-12-26 05:02:44
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
from Mem import createobject, reinitialize, objects, processcreate, getcurrentobjects, processdelete
import world
import sys, csv, os, random
import tkinter as tk
from tkinter import filedialog
global objTypes
objTypes = ['Eplanet', 'Jplanet', 'starO', 'starG']


class Menu:
    def __init__(self):
        self.changeButtonSW = True

    def init(self):
        self.errorWarnings = {}
        size = (0, 0.99, -1.3, 1)
        self.StarMenu = DirectScrolledFrame(relief=0,
                                            frameSize=(0, 0.99, -1.1, 1),
                                            canvasSize=size,
                                            pos=(0.79, 0, 0),
                                            scrollBarWidth=0.04)
        self.StarMenucanvas = self.StarMenu.getCanvas()
        self.StarMenucanvasParent = self.StarMenucanvas.getParent()
        path0 = getPath() + '/res/texture/gui-texture/'
        self.timeRateBar = DirectScrollBar(
            parent=self.StarMenu,
            value=20,
            range=(0, 80),
            pageSize=2,
            scrollSize=1,
            pos=(-1, 0, 0.92),
            frameSize=(-0.6, 0.6, -0.045, 0),
            frameColor=(0.2, 0.43, 0.88, 0.2),
            manageButtons=True,
            resizeThumb=True,
            command=self.changeTimeRate,
            thumb_relief=1,
            thumb_frameTexture=path0 + 'pr.jpg',
            incButton_relief=1,
            incButton_frameTexture=path0 + 'timr.jpg',
            decButton_relief=1,
            decButton_frameTexture=path0 + 'timl.jpg')
        self.timeLabel = DirectLabel(
            parent=self.timeRateBar,
            text=
            '\1purp\1* Time Proportional Scale *\2\n\1white\1|                |                |\n10^5           10^6            10^7           10^8           10^9\2',
            relief=0,
            scale=0.06,
            pos=(0, 0, 0.02))

        self.generateFixedCards()
        self.generateLine()
        self.changeButtonSwitch()

    def changeButtonSwitch(self):
        if self.changeButtonSW is True:
            self.Ch_button = DirectButton(parent=self.StarMenu,
                                          relief=1,
                                          scale=0.252,
                                          pos=(-0.3, 0, -0.9),
                                          text='Change',
                                          text_scale=0.25,
                                          command=self.changeButtonHandler)
        else:
            self.Ch_button = DirectButton(parent=self.StarMenu,
                                          relief=1,
                                          scale=0.252,
                                          pos=(-0.3, 0, -0.9),
                                          text='Done',
                                          text_scale=0.25,
                                          command=self.changeButtonHandler)

    def changeButtonHandler(self):
        if self.changeButtonSW is True:
            global World
            global WorldSwitch
            World.end()
            WorldSwitch.switchStatus = 1
            update()
            self.StarMenu.destroy()
            self.init()
            self.open()
            self.changeButtonSW = False
        else:
            self.StarMenu.destroy()
            self.init()
            self.open()
            self.changeButtonSW = True

    def open(self):
        global World
        World.takeMouseAway()
        self.StarMenu.show()
        global StarCards
        StarCards.init()

    def hide(self):
        global World
        World.takeMouseBack()
        self.StarMenu.hide()

    def changeTimeRate(self):
        rateGot = self.timeRateBar['value']
        rateGot = 1 / (2**(int(rateGot / 8)))
        global World
        World.changeTimeRate(rateGot)

    def generateFixedCards(self):
        self.typeCard = {}
        self.typeframe = {}
        self.starImgs = {}
        global objTypes
        starImgPath = getPath() + '/res/card/starImg/'
        for i in range(4):
            self.starImgs[objTypes[i]] = base.loader.loadTexture(starImgPath +
                                                                 objTypes[i] +
                                                                 '.jpg')
        typeText = [
            '\1light\1Earth like Planet\2', '\1light\1Jupiter like planet\2',
            '\1light\1O-type Star\2', '\1light\1G-type Star\2'
        ]
        path = getPath() + '/res/card/fixedCard/'
        for i in range(4):
            self.typeframe[objTypes[i]] = DirectFrame(
                parent=self.StarMenucanvas,
                frameSize=(0, 0.955, -0.26, 0),
                pos=(0, 0, 1 - 0.27 * i),
                relief=1,
                frameTexture=path + objTypes[i] + '.jpg',
                image_scale=0.25,
                text=typeText[i],
                text_pos=(0.7, -0.23, 0),
                text_scale=0.05)
            self.typeCard[objTypes[i]] = DirectCheckButton(
                parent=self.typeframe[objTypes[i]],
                relief=0,
                boxRelief=1,
                boxImage=self.starImgs[objTypes[i]],
                scale=0.128,
                pos=(0.264, 0, -0.13),
                command=self.generateDetailCard,
                extraArgs=[objTypes[i], True])

    def generateLine(self):
        self.divideLineframe = DirectFrame(parent=self.StarMenucanvas,
                                           frameSize=(0, 0.965, -0.02, 0),
                                           pos=(0, 0, -0.073),
                                           frameColor=(0.5, 0.5, 0.5, 1),
                                           relief=2)
        self.divideLine = OnscreenText(parent=self.divideLineframe,
                                       text='\1white\1.\2' * 42,
                                       scale=0.1,
                                       pos=(0.47, -0.011, 0))

    def generateDetailCard(self, choice, objtype, newStar, star=None):
        global KeyReg
        KeyReg.unregkeys()
        global Tipmgr
        Tipmgr.VariousTip()

        try:
            self.detailCardFrame.destory()
        except:
            pass
        try:
            if self.Filepath:
                pass
        except:
            self.Filepath = None
        self.detailCardFrame = DirectFrame(parent=self.StarMenu,
                                           relief=1,
                                           frameSize=(0, 0.8, -1, 1),
                                           frameColor=(0.7, 0.7, 0.2, 1),
                                           pos=(-2.58, 0, 0))
        path = getPath() + '/res/card/detailCard/' + objtype + '.jpg'
        self.detailCardFrame['frameTexture'] = path
        entries_title = [
            'Name', 'mass\t\t   kg', 'radius\t\t   km', 'x\t\t\tkm',
            'y\t\t\tkm', 'z\t\t\tkm', 'V_x\t\t\tkm/s', 'V_y\t\t\tkm/s',
            'V_z\t\t\tkm/s'
        ]
        self.entryList, self.textList = [], []

        def Name(num):
            t = DirectEntry(parent=self.detailCardFrame,
                            scale=0.063,
                            width=8,
                            relief=1,
                            pos=(0.1, 0, 0.8))
            self.entryList.append(t)
            t = OnscreenText(parent=self.entryList[num],
                             text=entries_title[num],
                             scale=0.7,
                             pos=(1.5, 1.5, 0),
                             fg=(0.5, 1, 0.9, 1))
            self.textList.append(t)

        def MassandRadius(num):
            t = DirectEntry(parent=self.detailCardFrame,
                            scale=0.06,
                            width=5,
                            relief=1,
                            pos=(0.17, 0, 0.7 - 0.17 * num))
            self.entryList.append(t)
            t = OnscreenText(parent=self.entryList[num],
                             text=entries_title[num],
                             scale=0.7,
                             pos=(2, 0, 0),
                             fg=(0.5, 1, 0.9, 1))
            self.textList.append(t)

        def CorandVel(num):
            t = DirectEntry(parent=self.detailCardFrame,
                            scale=0.06,
                            width=7,
                            relief=1,
                            pos=(0.17, 0, 0.7 - 0.17 * num))
            self.entryList.append(t)
            t = OnscreenText(parent=self.entryList[num],
                             text=entries_title[num],
                             scale=0.7,
                             pos=(3.6, 0, 0),
                             fg=(0.5, 1, 0.9, 1))
            self.textList.append(t)

        for num in range(9):
            if num == 0:
                Name(num)
            else:
                if num < 3:
                    MassandRadius(num)
                else:
                    CorandVel(num)
        if newStar:
            pass
        else:
            dataS = [
                star.name, star.mass, star.radius, star.cor[0], star.cor[1],
                star.cor[2], star.vel[0], star.vel[1], star.vel[2]
            ]
            for num in range(9):
                self.entryList[num].enterText(str(dataS[num]))

        self.closeEntry = YesNoDialog(
            parent=self.detailCardFrame,
            buttonValueList=[0, 1],
            buttonTextList=['\1blgr\1Close\2', '\1blgr\1Done\2'],
            button_relief=2,
            scale=0.8,
            pos=(0.56, 0, -0.75),
            relief=0,
            command=self.detailedCardHandler,
            extraArgs=[objtype, newStar, star])
        self.textureSet = OkDialog(parent=self.detailCardFrame,
                                   buttonTextList=['\1pink\1Various\2'],
                                   button_relief=2,
                                   scale=0.8,
                                   pos=(0.56, 0, -0.64),
                                   relief=0,
                                   command=self.detailedCardVariousTexture)
        self.textureSet['button_frameTexture'] = self.detailCardFrame[
            'frameTexture']
        self.closeEntry['button_frameTexture'] = self.detailCardFrame[
            'frameTexture']

    def detailedCardVariousTexture(self, choice):
        root = tk.Tk()
        root.withdraw()
        self.Filepath = filedialog.askopenfilename()

    def detailedCardHandler(self, button, objtype, newStar, star=None):
        for i in self.errorWarnings:
            self.errorWarnings[i].destroy()
        legitimate = True
        if button == 1:  # 'Done'
            dataS = []
            dataS.append(self.entryList[0].get())
            for le in range(1, 9):
                dataS.append(self.entryList[le].get())
                acceptText = '\1roman\1\1green\1Change Accepted\2\2'
                rejectText = '\1roman\1\1red\1Change Rejected\2\2'
                try:
                    dataS[le] = float(dataS[le])
                    t = OnscreenText(parent=self.entryList[le],
                                     text=acceptText,
                                     scale=0.68,
                                     pos=(2.85, -1, 0))
                    self.errorWarnings[le] = t
                except:
                    t = OnscreenText(parent=self.entryList[le],
                                     text=rejectText,
                                     scale=0.68,
                                     pos=(2.85, -1, 0))
                    legitimate = False
                    self.errorWarnings[le] = t
            if legitimate:
                reinitialize()
                if newStar is False:
                    if dataS[0] is None:
                        dataS[0] = 'Default Object'
                    else:
                        pass
                    star.name, star.mass, star.radius,
                    star.cor[0], star.cor[1], star.cor[2],
                    star.vel[0], star.vel[1], star.vel[2],
                    star.texture = dataS + [self.Filepath]
                else:
                    if dataS[0] is None:
                        dataS[0] = '\1white\1Default Object\2'
                    else:
                        pass
                    processcreate(objtype=objtype,
                                  texture=self.Filepath,
                                  myname=dataS[0],
                                  mass=dataS[1],
                                  radius=dataS[2],
                                  vel=[dataS[6], dataS[7], dataS[8]],
                                  cor=[dataS[3], dataS[4], dataS[5]])
                    canvasSize = (0, 0.996,
                                  self.StarMenu['canvasSize'][2] - 0.675, 1)
                self.detailCardFrame.destroy()
                global KeyReg
                KeyReg.regKey()
                global Tipmgr
                Tipmgr.endVariousTip(0)
                global StarCards
                StarCards.init()
            else:
                pass
        elif button == 0:  # "Close"
            self.detailCardFrame.destroy()
            KeyReg.regKey()
            Tipmgr.endVariousTip(0)


class starCards:
    def __init__(self):
        self.Cards = {}

    def init(self):
        for i in self.Cards:
            self.Cards[i].destroy()
        self.Cards = {}
        global MenuIns
        self.StarMenucanvas = MenuIns.StarMenucanvas
        self.objs = getcurrentobjects()
        self.generateCard()

    def selectRandomTexture(self, objtype):
        if objtype == 'starO':
            return self.selectRandomFile(getPath() + '/res/card/starO/')
        elif objtype == 'starG':
            return self.selectRandomFile(getPath() + '/res/card/starG/')
        elif objtype == 'Jplanet':
            return self.selectRandomFile(getPath() + '/res/card/Jplanet/')
        elif objtype == 'Eplanet':
            return self.selectRandomFile(getPath() + '/res/card/Eplanet/')

    def selectRandomFile(self, fileDir):
        pt = Filename(fileDir).toOsSpecific()
        pathDir = os.listdir(pt)
        selectedPic = random.sample(pathDir, 1)
        fileselected = Filename.fromOsSpecific(os.path.join(
            pt, selectedPic[0])).getFullpath()
        return fileselected

    def generateCard(self):
        for obj in self.objs:
            info = '\1roman\1mass: %d   kg\nradius: %d   km\2' % (obj.mass,
                                                                  obj.radius)
            if obj.texture2D:
                pass
            else:
                obj.texture2D = self.selectRandomTexture(obj.objtype)

            if not self.Cards:
                card = DirectFrame(
                    pos=(0, 0, -0.093),
                    parent=self.StarMenucanvas,
                    frameTexture=obj.texture2D,
                    frameSize=(0.02, 0.95, -0.35, 0),
                )
                self.Cards[obj.ID] = card
                lastobj = obj
            else:
                if lastobj.switch is False:
                    delta = -0.690
                else:
                    delta = -0.365
                card = DirectFrame(
                    pos=(0, 0, delta),
                    parent=self.Cards[lastobj.ID],
                    frameTexture=obj.texture2D,
                    frameSize=(0.02, 0.95, -0.35, 0),
                )
                self.Cards[obj.ID] = card
                lastobj = obj
            path = getPath() + '/res/card/starImg/'
            myButton = DirectCheckButton(parent=card,
                                         boxRelief=1,
                                         boxBorder=0,
                                         boxImage=path + obj.objtype + '.jpg',
                                         scale=0.174,
                                         pos=(0.378, 0, -0.174),
                                         relief=0,
                                         command=self.openDetailCard,
                                         extraArgs=[obj])
            myInfo = OnscreenText(parent=card,
                                  text=info,
                                  mayChange=1,
                                  align=TextNode.ACenter,
                                  pos=(0.675, -0.2, 0),
                                  scale=0.055,
                                  fg=(0.7, 0.5, 1, 1))
            myName = OnscreenText(parent=myInfo,
                                  text=obj.name,
                                  mayChange=1,
                                  align=TextNode.ACenter,
                                  pos=(0.675, -0.12, 0),
                                  scale=0.058,
                                  fg=(0.96, 0.97, 1, 1))
            if obj.switch is True:
                infoCard = DirectFrame(parent=card,
                                       frameTexture=card['frameTexture'],
                                       frameSize=(0, 0.91, -0.32, 0),
                                       relief=1)
                infoCard.setPos(0.025, 0, -0.35)

                velo, posi = list(range(3)), list(range(3))
                vl = ['\1roman\1vx\2', '\1roman\1vy\2', '\1roman\1vz\2']
                ps = ['\1roman\1x\2', '\1roman\1y\2', '\1roman\1z\2']
                v, p = obj.vel, obj.cor
                for i in range(3):
                    velo[i] = DirectEntry(
                        parent=infoCard,
                        initialText='{:'
                        '>8}'.format(int(v[i])) +
                        '{:.3f}'.format(v[i] - int(v[i]))[1:],
                        scale=.035,
                        pos=(0.055 + i * 0.234, 0, -0.218),
                        relief=1,
                        width=5.2,
                    )
                    vl[i] = OnscreenText(parent=velo[i],
                                         text=vl[i],
                                         scale=1.2,
                                         pos=(-0.7, 0, 0),
                                         fg=(0.5, 1, 0.9, 1))
                V = OnscreenText(parent=velo[1],
                                 text='\1roman\1Velocity\2',
                                 scale=1.2,
                                 pos=(2.5, 1.7, 0),
                                 align=TextNode.ACenter,
                                 fg=(0.9, 0.85, 0.14, 1))
                UnV = OnscreenText(parent=velo[2],
                                   text='\1roman\1\1blgr\1km/s\2\2',
                                   scale=1.2,
                                   pos=(6.7, 0, 0))
                for j in range(3):
                    posi[2 - j] = DirectEntry(
                        parent=infoCard,
                        initialText='{:'
                        '>8}'.format(int(p[i])) +
                        '{:.3f}'.format(p[i] - int(p[i]))[1:],
                        scale=.035,
                        pos=(0.055 + (2 - j) * 0.234, 0, -0.11),
                        relief=1,
                        width=5.2,
                    )
                    ps[2 - j] = OnscreenText(parent=posi[2 - j],
                                             text=ps[2 - j],
                                             scale=1.2,
                                             pos=(-0.9, 0, 0),
                                             fg=(0.5, 1, 0.9, 1))
                P = OnscreenText(parent=posi[1],
                                 text='\1roman\1Position\2',
                                 scale=1.2,
                                 pos=(2.5, 1.7, 0),
                                 align=TextNode.ACenter,
                                 fg=(0.9, 0.14, 0.85, 1))
                UnP = OnscreenText(parent=posi[2],
                                   text='\1roman\1\1blgr\1km\2\2',
                                   scale=1.2,
                                   pos=(6.7, 0, 0))
                global MenuIns
                if MenuIns.changeButtonSW is False:
                    myTr = YesNoCancelDialog(parent=infoCard,
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
                                             command=self.closeDetailCard,
                                             extraArgs=[obj])
                else:
                    myTr = OkDialog(parent=infoCard,
                                    relief=0,
                                    scale=0.62,
                                    button_relief=0,
                                    buttonTextList=['\1blgr\1Close\2'],
                                    buttonValueList=[-1],
                                    button_scale=1.1,
                                    pos=(0.67, 0, -0.186),
                                    command=self.closeDetailCard,
                                    extraArgs=[obj])
            else:
                pass

    def openDetailCard(self, choice, obj):
        obj.switch = True
        global MenuIns
        MenuIns.StarMenu.destroy()
        MenuIns.init()
        MenuIns.open()

    def closeDetailCard(self, choice, obj):
        if choice == -1:
            obj.switch = False
            global MenuIns
            MenuIns.StarMenu.destroy()
            MenuIns.init()
            MenuIns.open()
        elif choice == 0:
            MenuIns.generateDetailCard(0, obj.objtype, False, star=obj)
        else:
            processdelete(obj)
            reinitialize()
            self.objs = getcurrentobjects()
            MenuIns.StarMenu.destroy()
            MenuIns.init()
            MenuIns.open()


def update():
    global StarCards
    StarCards.init()


class worldSwitch:
    def __init__(self):
        global World
        self.switchStatus = 1

    def switch(self):
        global statusText
        if self.switchStatus == 1:
            statusText['text'] = '\1white\1The world is \2\1red\1running\2'
            objs = getcurrentobjects()
            if not objs:
                return None
            else:
                base.taskMgr.add(World.start, 'start')
                self.switchStatus = 2
        elif self.switchStatus == -1:
            statusText['text'] = '\1white\1The world is \2\1red\1not running\2'
            World.end()
            self.switchStatus = -2

    def changeStarttingStatus(self):
        if self.switchStatus == 2:
            self.switchStatus = -1
        elif self.switchStatus == -2:
            self.switchStatus = 1


def changeStarttingStatusout():
    global WorldSwitch
    WorldSwitch.changeStarttingStatus()
    # TODO callback


class guiRenderReg:
    def __init__(self):
        self.tp = TextPropertiesManager.getGlobalPtr()
        self.setWordStyle()

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


class menuSwitch:
    def __init__(self):
        self.trigger = True

    def switch(self):
        global MenuIns, statusText
        if self.trigger is False:
            self.trigger = True
            MenuIns.open()
            statusText.show()
        elif self.trigger is True:
            self.trigger = False
            MenuIns.hide()
            statusText.hide()


class keyRegMgr:
    def __init__(self):
        global WorldSwitch, MenuSwitch
        WorldSwitch = worldSwitch()
        MenuSwitch = menuSwitch()
        base.accept('r', WorldSwitch.switch)
        base.accept('q', MenuSwitch.switch)
        base.accept('control-e', sys.exit)

    def regKey(self):
        base.accept('r', WorldSwitch.switch)
        base.accept('q', MenuSwitch.switch)

    def unregkeys(self):
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
        try:
            if self.Varioustip:
                return None
        except:
            pass
        if self.statusDict['NoVtip'] == '1':
            return
        else:
            t_k3 = 'You can click \1pink\1\"Various\"\2 to design you own star!!!\n\nAnd notice English input is acceptable'
            self.Varioustip = YesNoDialog(
                text=t_k3,
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
        try:
            self.Varioustip.destroy()
        except:
            pass


class gui(ShowBase):
    def __init__(self):
        self.setup()
        guiRenderReg()
        global KeyReg
        KeyReg = keyRegMgr()
        self.welcome()

    def init(self):
        global World
        global statusText
        global initTextObject, StartButton
        World = world.world()
        initTextObject.destroy()
        StartButton.destroy()
        global Tipmgr
        Tipmgr = TipMgr()
        Tipmgr.moveTip()
        global MenuIns
        MenuIns = Menu()
        MenuIns.init()
        global StarCards
        StarCards = starCards()
        t_k = '\1white\1The world is \2\1red\1not running\2'
        statusText = OnscreenText(
            text=t_k,
            pos=(0.3, -0.97, 0),
            scale=0.06,
            mayChange=True,
        )

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
