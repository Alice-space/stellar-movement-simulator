'''
@Author: Alicespace
@Date: 2019-12-16 08:22:23
@LastEditTime : 2019-12-25 19:58:11
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
import world
import sys, csv, os, random
import tkinter as tk
from tkinter import filedialog

#tips or welcome
t_k1 = 'Choose a card and click it to define your star'
t_k2 = 'Press \"R\" to run\n\n  Press \"Q\" to hide the Menu\n\n    Press \"ctrl+e\" to exit'
t_k3 = 'You can click \1pink\1\"Various\"\2 to design you own star!!!\n\nAnd notice English input is acceptable'
t_k0 = "\1roman\1\1slant\1Hello! Welcome to our\n\1blood\1Stellar MoveMent Simulator\2\2\n \
\1 slant\1Hope you enjoy yourself\2"

#tools
path = 'res/card/'
path0 = 'res/texture/gui-texture/'
starPath = [
    'res/texture/Eplanet/', 'res/texture/Jplanet/', 'res/texture/starO/',
    'res/texture/starG'
]
purp, gray, pink, blgr, light, green, blue, blood, erro, cutoff, Roman = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
im, star1, star2, e_planet, g_planet, default_texture = 1, 1, 1, 1, 1, 1

#some mess and their explanation
timeRateBar = 1
tip = ''  #str object for checking whether to give tips or not
ftip, stip, ttip = 1, 2, 3  #tips
Filepath = default_texture  #filepath to load texture(temporary)
f, bv = 0, 0  #arg to see if file is chosen(temporary)
initTextObject, StartButton = 1, 1  #Welcom direct
StarMenu, StarMenucanvas = 1, 1  #Main menu and its canvas to move
size = (0, 0.99, -1.3, 1)  #Initial StarMenu['frameSize']
entryList, entryErroList = 1, 1  #While creating a card(temporary)
typeCard, typeframe = list(range(4)), list(range(4))  #4 types of stars
creatCard, Lazy = 1, 1  #Datas inquiry to create a card(once a time, usually destroied
sd = list('h' * 9)  #Datas(temporary)
ListS = []
StarCopy,mycard,MyStar,Cframe,ChArg,velo,posi=[],[],[],[],[],[],[]
#Stars' name ,card ,exactlly what the stars are,information card,
#argument to help see if the Cframe is open,
#velocity and position datas of all stars(Though they are just entries)
#main to import


def switch():
    global sw, world
    if sw == 1:
        try:
            world.start()
        except:
            pass
        sw = sw * (-1)
    else:
        try:
            world.end()
        except:
            pass
        sw = sw * (-1)


class gui(ShowBase):
    def __init__(self):
        loadPrcFileData('', 'fullscreen false')
        wp = WindowProperties()
        wp.setSize(1920, 1080)
        base.win.requestProperties(wp)
        base.accept('control-e', self.exits)
        self.checkInit()
        self.Tools()
        self.Welcome()
        global sw
        sw = 1

    def exits(self):
        base.destroy()
        sys.exit()

    def Welcome(self):  #welcom
        global initTextObject, StartButton
        initTextObject = OnscreenText(text=t_k0,
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
                                   command=self.begin)

    #TextProperty, various textproperties are assigned here
    def Tools(self):
        global im,star1,star2,e_planet,g_planet,\
               default_texture,path,purp,gray,pink,blgr, light, green, blue, blood, erro, cutoff, Roman
        tp = TextPropertiesManager.getGlobalPtr()

        class prop():
            def font(self, filepath, name):
                self.font = loader.loadFont(filepath)
                tpF = TextProperties()
                tpF.setFont(self.font)
                tp.setProperties(name, tpF)

            def fg(self, name, r, g, b, a):
                tpG = TextProperties()
                tpG.setTextColor(r, g, b, a)
                tp.setProperties(name, tpG)

        path = 'res/card/'
        try:
            purp, gray, pink, blgr, light, green, blue, blood, erro, cutoff, Roman = prop(
            ), prop(), prop(), prop(), prop(), prop(), prop(), prop(), prop(
            ), prop(), prop()
            purp.fg('purp', 0.8, 0.57, 0.95, 3.4)
            gray.fg('gray', 0.76, 0.75, 0.77, 1)
            pink.fg('pink', 0.86, 0.25, 0.6, 1)
            light.fg('light', 0.8, 1, 0.5, 2)
            blgr.fg('blgr', 0.5, 1, 0.9, 1.4)
            green.fg('green', 0, 0.4, 1, 1.5)
            blue.fg('blue', 0.3, 0.5, 0.65, 1)
            blood.fg('blood', 0.83, 0.39, 0.44, 2)
            erro.fg('red', 1, 0.2, 0, 2)
            cutoff.fg('white', 1, 1, 1, 1)
            Roman.font('cmtt12', 'roman')
        except:
            pass
        star1,star2,e_planet,g_planet=loader.loadTexture( path+'11411.jpg'),\
                                loader.loadTexture(path+'11511.jpg'),\
                                loader.loadTexture(path+'11211.jpg'),\
                                loader.loadTexture(path+'11311.jpg')
        #default_texture = [starPath[0]+'default.jpg',starPath[1]+'default.jpg',starPath[2]+'default.jpg',starPath[3]+'default.jpg']
        im = [e_planet, g_planet, star1, star2]

    def checkInit(self):  #get tip in the csv file to use later
        global tip
        if os.path.exists('res/config/Tips.csv'):
            with open(
                    'res/config/Tips.csv',
                    'r',
            ) as tips:
                reader = csv.reader(tips)
                for line in reader:
                    for i in range(len(line)):
                        tip += line[i]
        else:
            pass

    def begin(self):  #the world begin to load and open menu
        global world
        world = world.world()
        initTextObject.destroy()
        StartButton.destroy()
        if 'Ftip' in tip:
            pass
        else:
            Ftip()
        OpenMenu()


def Ftip():  #first tip
    global ftip
    ftip = YesNoDialog(text=t_k1,
                       scale=1,
                       pos=(-0.02, 0, 0.22),
                       buttonTextList=['No tips', '\tNext'],
                       buttonValueList=[0, 1],
                       midPad=0.17,
                       button_relief=0,
                       relief=1,
                       command=Stip)


def Stip(x):  #second tip
    global stip
    if x:
        pass
    else:
        with open('res/config/Tips.csv', 'a') as tips:
            writer = csv.writer(tips)
            writer.writerow('Ftip')
    try:
        ftip.destroy()
    except:
        pass
    if 'Stip' in tip:
        pass
    else:
        stip = YesNoCancelDialog(text=t_k2,
                                 scale=1,
                                 pos=(-0.02, 0, 0.22),
                                 buttonTextList=['No tips', '\tLast', 'Next'],
                                 buttonValueList=[0, -1, 1],
                                 midPad=0.1,
                                 button_relief=0,
                                 relief=1,
                                 command=tip_pau)


def tip_pau(x):  #a tip pause
    stip.destroy()
    if x == 0:
        with open('res/config/Tips.csv', 'a') as tips:
            writer = csv.writer(tips)
            writer.writerow('Stip')
    elif x == -1:
        Ftip()


def Ttip():  #third tip
    global ttip
    ttip = YesNoDialog(text=t_k3,
                       scale=1,
                       pos=(-0.02, 0, 0.22),
                       buttonTextList=['No tips', '\tClose'],
                       buttonValueList=[0, 1],
                       midPad=0.15,
                       button_relief=0,
                       relief=1,
                       command=tip_spau)


def tip_spau(x):  #second tip pause
    if x:
        pass
    else:
        with open('res/config/Tips.csv', 'a') as tips:
            writer = csv.writer(tips)
            writer.writerow('Ttip')
    ttip.destroy()


def OpenMenu():  #the menu(a scolled frame)
    global StarMenu, StarMenucanvas,timeRateBar
    global world
    try:
        world.takeMouseAway()
    except:
        pass
    StarMenu = DirectScrolledFrame(relief=0,
                                   frameSize=(0, 0.99, -1.1, 1),
                                   canvasSize=size,
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
                                  command=CRT,
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
    try:
        MyStar[0].Card(0)
    except:
        pass

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
    base.accept('q', hideMenu)
    base.accept('r', switch)

def CRT():
    rate = timeRateBar['value']
    rate = 10**int(rate / 20)
    world.changeTimeRate(rate)


def hideMenu():
    global StarMenu, world
    StarMenu.hide()
    world.takeMouseBack()
    base.accept('q', showMenu)


def showMenu():
    global StarMenu, world
    StarMenu.show()
    world.takeMouseAway()
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
            boxImage=im[i],
            scale=0.128,
            pos=(0.264, 0, -0.13),
            command=creat,
            extraArgs=[i])  #i is the order of the type


def creat(x, i, n=0, y=0.1):  #generate a frame to get args
    global creatCard, entryList, entryErroList, sd, f, bv, Filepath
    if bv:
        pass
    else:
        if 'Ttip' in tip:
            pass
        else:
            Ttip()
    try:
        creatCard.frame.destroy()
    except:
        pass
    sd, f, bv = list('h' * 9), 0, 1
    try:
        Filepath = MyStar[y].texture
    except:
        Filepath = None
    creatCard = geneFrame(StarMenu, (0, 0.8, -1, 1), (-2.58, 0, 0),
                          (0.7, 0.7, 0.2, 1), 1)
    creatCard.frame['frameTexture'] = path + 'z' + str(i + 1) + '.jpg'
    t_kentry = [
        'Name it!', 'mass\t\t   kg', 'radius\t\t   km', 'x\t\t\tkm',
        'y\t\t\tkm', 'z\t\t\tkm', 'v_x\t\t\tkm/s', 'v_y\t\t\tkm/s',
        'v_z\t\t\tkm/s'
    ]
    entryList, text, entryErroList = list(range(9)), list(range(9)), list(
        range(9))
    for le in range(9):
        if le != 0:
            if le < 3:
                entryList[le] = geneEntry(creatCard.frame, 0.06,
                                          (0.17, 0, 0.7 - 0.17 * le), 5, 1,
                                          None, [le])
                text[le] = OnscreenText(parent=entryList[le].entry,
                                        text=t_kentry[le],
                                        scale=0.7,
                                        pos=(2, 0, 0),
                                        fg=(0.5, 1, 0.9, 1))
            else:
                entryList[le] = geneEntry(creatCard.frame, 0.06,
                                          (0.17, 0, 0.7 - 0.17 * le), 7, 1,
                                          None, [le])
                text[le] = OnscreenText(parent=entryList[le].entry,
                                        text=t_kentry[le],
                                        scale=0.7,
                                        pos=(3.6, 0, 0),
                                        fg=(0.5, 1, 0.9, 1))
        else:
            entryList[le] = geneEntry(creatCard.frame, 0.063, (0.1, 0, 0.8), 8,
                                      1, None, [le])
            text[le] = OnscreenText(parent=entryList[le].entry,
                                    text=t_kentry[le],
                                    scale=0.7,
                                    pos=(1.5, 1.5, 0),
                                    fg=(0.5, 1, 0.9, 1))
    if n:
        stars = MyStar[y]
        dataS = [
            stars.name, stars.mas, stars.rad, stars.pos[0], stars.pos[1],
            stars.pos[2], stars.vel[0], stars.vel[1], stars.vel[2]
        ]
        for le in range(9):
            entryList[le].entry.enterText(str(dataS[le]))

    closeEntry = YesNoDialog(
        parent=creatCard.frame,
        buttonTextList=['\1blgr\1Close\2', '\1blgr\1Done\2'],
        buttonValueList=[0, 1],
        scale=0.8,
        pos=(0.56, 0, -0.7511),
        relief=0,
        button_relief=2,
        command=closeE,
        extraArgs=[i, y, n])
    textureSet = OkDialog(parent=creatCard.frame,
                          buttonTextList=['\1pink\1Various\2'],
                          scale=0.8,
                          pos=(0.56, 0, -0.64),
                          relief=0,
                          button_relief=2,
                          command=choseTexture)
    textureSet['button_frameTexture'] = closeEntry[
        'button_frameTexture'] = creatCard.frame['frameTexture']
    base.ignore('q')
    base.ignore('r')


def choseTexture(x):  #give a tk or list to choose texture
    global Filepath, f
    root = tk.Tk()
    root.withdraw()
    Filepath = filedialog.askopenfilename()  #获得选择好的文件
    f = 1


def closeE(x, i, y, n=0):
    #close the args assignment frame and creste object
    global rr, ListS, entryList, entryErroList, creatCard, MyStar, StarCopy, ChArg, Cframe, velo, posi, size, StarMenu, Type
    dd = 1
    Type = ['Eplanet', 'Jplanet', 'starO', 'starG']
    if x:
        sd[0] = entryList[0].entry.get()
        for le in range(1, len(sd)):
            sd[le] = entryList[le].entry.get()
            try:
                sd[le] = float(sd[le])
                entryErroList[le] = geneText(entryList[le].entry,
                                             '\1roman\1\1green\1Yes!\2\2',
                                             0.68, (0.8, -1, 0))
            except:
                entryErroList[le] = geneText(entryList[le].entry,
                                             '\1roman\1\1red\1wrong\2\2', 0.68,
                                             (0.8, -1, 0))
            if entryErroList[le].text['text'] == '\1roman\1\1red\1wrong\2\2':
                dd = 0
                continue
        if dd:
            texture = Filepath
            if n:
                # change
                MyStar[y] = StarCard(sd[0], sd[1], sd[2], [sd[3], sd[4], sd[5]],
                                [sd[6], sd[7], sd[8]], i, texture)
                StarCopy[y] = sd[0]
                reinitialize(
                )
                MEM.getcurr
                zhi jie gai 
                obj.cor
                obj.vel
                obj.objdata = deque([0,vel1,vel2,vel3,cor[]])
                obj.texture

                for star in MyStar:
                    processcreate(Type[i],
                                 MyStar[y].texture,
                                 myname=star.name,
                                 mass=star.mas,
                                 radius=star.rad,
                                 vel=star.vel,
                                 cor=star.pos)

            else:
                createobject(Type[i],
                             Filepath,
                             myname=sd[0],
                             mass=sd[1],
                             radius=sd[2],
                             vel=[sd[6], sd[7], sd[8]],
                             cor=[sd[3], sd[4], sd[5]])
                if not sd[0]:
                    sd[0] = 'Hapy'
                star = StarCard(sd[0], sd[1], sd[2], [sd[3], sd[4], sd[5]],
                                [sd[6], sd[7], sd[8]], i, Filepath)
                MyStar.append(star)  #object
                StarCopy.append(star.name)  #name of object
                ChArg.append(0)  #open or not index
                Cframe.append(1)  #inspect data
                velo.append(1)  #vel_entry
                posi.append(1)  #posi_entry
                Length = StarMenu['canvasSize']
                size = (0, 0.996, Length[2] - 0.675, 1)
            StarMenu.destroy()
            OpenMenu()  #update the menu
            creatCard.frame.destroy()
            base.accept('r', switch)
            base.accept('q', hideMenu)

    else:
        creatCard.frame.destroy()
        base.accept('q', hideMenu)


#generate some widgets
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


class StarCard(ShowBase):
    def __init__(self, name, mas, rad, pos, vel, ty, ture):
        self.name = name
        self.mas = mas
        self.rad = rad
        self.pos = pos
        self.vel = vel
        self.ty = ty
        self.texture = ture

    def Card(self, x):  #generate a card
        global mycard, Cframe, velo, posi
        myname = self.name
        mypos = self.pos
        myvel = self.vel
        mystyle = self.ty
        tk_1='\1roman\1mass: %d   kg\nradius: %d   km\2'\
              %(self.mas,self.rad)
        para = MyStar.index(self)
        ima = chr(mystyle + 97)
        luck = random.randint(1, 4)
        if ima == 'a':
            ima = chr(random.choice([97, 101, 98]))
        card = DirectFrame(pos=(0, 0, 0. - 0.093 - para * 0.365 - x),
                           frameTexture=path + ima + str(luck) + '.jpg',
                           frameSize=(0.02, 0.95, -0.35, 0),
                           frameColor=(0.65 - para * 0.13, 0.73 - para * 0.08,
                                       0.86 - para * 0.13, 1))
        card.reparentTo(StarMenucanvas)
        myCha = DirectCheckButton(parent=card,
                                  boxImage=im[mystyle],
                                  scale=0.174,
                                  pos=(0.378, 0, -0.174),
                                  relief=0,
                                  boxRelief=1,
                                  boxBorder=0,
                                  command=self.Change,
                                  extraArgs=[para, myvel, mypos])
        myMass = OnscreenText(parent=card,
                              text=tk_1,
                              mayChange=1,
                              align=TextNode.ACenter,
                              pos=(0.675, -0.2, 0),
                              scale=0.055,
                              fg=(0.7, 0.5, 1, 1))
        myName = OnscreenText(parent=myMass,
                              text=myname,
                              mayChange=1,
                              align=TextNode.ACenter,
                              pos=(0.675, -0.12, 0),
                              scale=0.058,
                              fg=(0.96, 0.97, 1, 1))
        if ChArg[para] == -1:
            try:
                b = ChArg[:para + 1].count(-1)
                MyStar[para + 1].Card(0.325 * b)
            except:
                pass
            Cframe[para] = DirectFrame(
                parent=card,
                frameTexture=mycard[para]['frameTexture'],
                frameSize=(0, 0.91, -0.32, 0),
                frameColor=(0.6 - para * 0.13, 0.7 - para * 0.08,
                            0.8 - para * 0.13, 1),
                relief=1)
            Cframe[para].setPos(0.025, 0, -0.35)

            velo[para], posi[para] = [1, 2, 3], [1, 2, 3]
            vl, ps = ['\1roman\1vx\2', '\1roman\1vy\2', '\1roman\1vz\2'
                      ], ['\1roman\1x\2', '\1roman\1y\2', '\1roman\1z\2']
            for i in range(3):
                velo[para][i] = DirectEntry(parent=Cframe[para],
                                            initialText=str(
                                                MyStar[para].vel[i]),
                                            scale=.035,
                                            pos=(0.055 + i * 0.234, 0, -0.218),
                                            relief=1,
                                            width=5.2)
                vl[i] = OnscreenText(parent=velo[para][i],
                                     text=vl[i],
                                     scale=1.2,
                                     pos=(-0.9, 0, 0),
                                     fg=(0.5, 1, 0.9, 1))
            V = OnscreenText(parent=velo[para][1],
                             text='\1roman\1Velocity\2',
                             scale=1.2,
                             pos=(2.5, 1.7, 0),
                             align=TextNode.ACenter,
                             fg=(0.9, 0.85, 0.14, 1))
            UnV = OnscreenText(parent=velo[para][2],
                               text='\1roman\1\1blgr\1km/s\2\2',
                               scale=1.2,
                               pos=(6.7, 0, 0))
            for j in range(3):
                posi[para][2 - j] = DirectEntry(
                    parent=Cframe[para],
                    initialText=str(MyStar[para].pos[2 - j]),
                    scale=.035,
                    pos=(0.055 + (2 - j) * 0.234, 0, -0.11),
                    relief=1,
                    width=5.2)
                ps[2 - j] = OnscreenText(parent=posi[para][2 - j],
                                         text=ps[2 - j],
                                         scale=1.2,
                                         pos=(-0.9, 0, 0),
                                         fg=(0.5, 1, 0.9, 1))
            P = OnscreenText(parent=posi[para][1],
                             text='\1roman\1Position\2',
                             scale=1.2,
                             pos=(2.5, 1.7, 0),
                             align=TextNode.ACenter,
                             fg=(0.9, 0.14, 0.85, 1))
            UnP = OnscreenText(parent=posi[para][2],
                               text='\1roman\1\1blgr\1km\2\2',
                               scale=1.2,
                               pos=(6.7, 0, 0))
            myTr = YesNoCancelDialog(parent=Cframe[para],
                                     relief=0,
                                     scale=0.62,
                                     button_relief=0,
                                     buttonTextList=[
                                         '\1blgr\1Close\2',
                                         '\1blgr\1Change Args\2',
                                         '\1blgr\1Delet\2'
                                     ],
                                     button_scale=1.1,
                                     pos=(0.5, 0, -0.186),
                                     buttonValueList=[-1, 0, 1],
                                     command=self.closeChange,
                                     extraArgs=[para])
        else:
            if para < len(MyStar) - 1:
                try:
                    mycard[para + 1].destroy()
                except:
                    pass
                b = ChArg[:para + 1].count(-1)
                MyStar[para + 1].Card(0.325 * b)

    def Change(self, x, y, v, p):  #inspect data
        global velo, posi, Cframe, mycard, ChArg, ListS, StarMenu
        StarMenu.destroy()
        OpenMenu()

        if ChArg[y] == -1:
            pass
        else:
            ChArg[y] = -1
            try:
                mycard[y + 1].destroy()
                b = ChArg[:y + 1].count(-1)
                MyStar[y + 1].Card(0.325 * b)
            except:
                pass
            Cframe[y] = DirectFrame(parent=mycard[y],
                                    frameTexture=mycard[y]['frameTexture'],
                                    frameSize=(0, 0.91, -0.32, 0),
                                    frameColor=(0.6 - y * 0.13, 0.7 - y * 0.08,
                                                0.8 - y * 0.13, 1),
                                    relief=1)
            Cframe[y].setPos(0.025, 0, -0.35)

            velo[y], posi[y] = [1, 2, 3], [1, 2, 3]
            vl, ps = ['\1roman\1vx\2', '\1roman\1vy\2', '\1roman\1vz\2'
                      ], ['\1roman\1x\2', '\1roman\1y\2', '\1roman\1z\2']
            for i in range(3):
                velo[y][i] = DirectEntry(parent=Cframe[y],
                                         initialText=str(v[i]),
                                         scale=.035,
                                         pos=(0.055 + i * 0.234, 0, -0.218),
                                         relief=1,
                                         width=5.2,
                                         extraArgs=[y, 2, i])
                vl[i] = OnscreenText(parent=velo[y][i],
                                     text=vl[i],
                                     scale=1.2,
                                     pos=(-0.9, 0, 0),
                                     fg=(0.5, 1, 0.9, 1))
            V = OnscreenText(parent=velo[y][1],
                             text='\1roman\1Velocity\2',
                             scale=1.2,
                             pos=(2.5, 1.7, 0),
                             align=TextNode.ACenter,
                             fg=(0.9, 0.85, 0.14, 1))
            UnV = OnscreenText(parent=velo[y][2],
                               text='\1roman\1\1blgr\1km/s\2\2',
                               scale=1.2,
                               pos=(6.7, 0, 0))
            for j in range(3):
                posi[y][2 - j] = DirectEntry(parent=Cframe[y],
                                             initialText=str(p[2 - j]),
                                             scale=.035,
                                             pos=(0.055 + (2 - j) * 0.234, 0,
                                                  -0.11),
                                             relief=1,
                                             width=5.2,
                                             extraArgs=[y, 1, j])
                ps[2 - j] = OnscreenText(parent=posi[y][2 - j],
                                         text=ps[2 - j],
                                         scale=1.2,
                                         pos=(-0.9, 0, 0),
                                         fg=(0.5, 1, 0.9, 1))
            P = OnscreenText(parent=posi[y][1],
                             text='\1roman\1Position\2',
                             scale=1.2,
                             pos=(2.5,1.7,0),
                             align=TextNode.ACenter,
                             fg=(0.9, 0.14, 0.85, 1))
            UnP = OnscreenText(parent=posi[y][2],
                               text='\1roman\1\1blgr\1km\2\2',
                               scale=1.2,
                               pos=(6.7, 0, 0))
            myTr = YesNoCancelDialog(parent=Cframe[y],
                                     relief=0,
                                     scale=0.62,
                                     button_relief=0,
                                     buttonTextList=[
                                         '\1blgr\1Close\2',
                                         '\1blgr\1Change Args\2',
                                         '\1blgr\1Delet\2'
                                     ],
                                     button_scale=1.1,
                                     pos=(0.5, 0, -0.186),
                                     buttonValueList=[-1, 0, 1],
                                     command=self.closeChange,
                                     extraArgs=[y])
            base.ignore('r')

    def closeChange(self, x, y):  #close Cframe and do what the user like
        global ChArg, MyStar, StarCopy, size
        if x == -1:
            Cframe[y].destroy()
            ChArg[y] = 0
            Review(y)
        elif x == 1:
            global world
            world.end()
            del StarCopy[y]
            del ChArg[y]
            del MyStar[y]
            mycard[y].destroy()
            del mycard[y]

            Review(y - 1)
            reinitialize()
            for star in MyStar:
                createobject(star.ty,
                             star.texture,
                             myname=star.name,
                             mass=star.mas,
                             radius=star.rad,
                             vel=star.vel,
                             cor=star.pos)
            world.start()

        else:
            creat(1, MyStar[y].ty, n=1, y=y)

        base.accept('r', switch)


def updating(objs,data):
    global velo, posi, MyStar, world, ListS, Type,mycard,Cframe,ChArg,size,StarMenu,StarCopy

    mycard=[]
    for obj in objs:
        star=StarCard(obj.name,
        obj.mass,
        obj.radius,
        data[obj.ID][4:7],
        data[obj.ID][1:4],
        obj.objtype,
        obj.texture)
        MyStar.append(star)
        StarCopy.append(star.name)
        ChArg.append(0)  #open or not index
        Cframe.append(1)  #inspect data
        velo.append(1)  #vel_entry
        posi.append(1)  #posi_entry
        Length = StarMenu['canvasSize']
        size = (0, 0.996, Length[2] - 0.675, 1)
        StarMenu.destroy()
        OpenMenu()  #update the menu    
        '''objs, Data = world.getData()
    if not Data:
        return task.again
    if objs == ListS:
        pass
    else:
        l = 0
        while l < len(ListS):
            if objs[l] == ListS[l]:
                l += 1
            else:
                del ListS[l]
                del StarCopy[l]
                del ChArg[l]
                del MyStar[l]
                mycard[l].destroy()
                del mycard[l]
                Review(l - 1)
        for y in range(len(objs)):
            if objs[y] in ListS:
                pass
            else:
                ListS.append(objs[y])
                starS = StarCard('Hapy', objs[y].mass, objs[y].radius,
                                 Data[objs[y].ID][4:7], Data[objs[y].ID][1:4],
                                 Type.index(objs[y].objtype), objs[y].texture)
                MyStar.append(starS)
                StarCopy.append(starS.name)
                Cframe.append(1)
                ChArg.append(0)
                velo.append(1)
                posi.append(1)
                starS.Card(0)

    for y in range(len(ChArg)):
        if ChArg[y] == -1:
            MyStar[y].vel = Data[y][1:4]
            MyStar[y].pos = Data[y][4:7]
            for i in range(3):
                posi[y][i].enterText('{:'
                                     '>8}'.format(int(MyStar[y].pos[i])) +
                                     '{:.3f}'.format(MyStar[y].pos[i] -
                                                     int(MyStar[y].pos[i])))
                velo[y][i].enterText('{:'
                                     '>8}'.format(int(MyStar[y].vel[i])) +
                                     '{:.3f}'.format(MyStar[y].vel[i] -
                                                     int(MyStar[y].vel[i])))
    return task.again'''


def Review(y, n=0):
    global mycard
    try:
        mycard[y + 1].destroy()
        b = ChArg[:y + 1].count(-1)
        MyStar[y + 1].Card(0.325 * b)
    except:
        pass
