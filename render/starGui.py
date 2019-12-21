'''
@Author: Alicespace
@Date: 2019-12-16 08:22:23
@LastEditTime : 2019-12-20 13:18:13
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
from calculate.Mem import createobject
from render import world
import sys, csv, os, random

t_k1 = 'Choose a card to define your star\n\n  press \"Esc\" to close the menu'
t_k2 = 'Thank you for pressing \"Enter\" while inputting Args'
t_k0 = "\1roman\1\1slant\1Hello! Welcome to our\n\1blood\1Stellar Motion Model\'\'\2\2\n \
\1slant\1Hope you enjoy yourself\2"

#TextProperty
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
blgr, light, green, blue, blood, erro, cutoff, Roman = prop(), prop(), prop(
), prop(), prop(), prop(), prop(), prop()
light.fg('light', 0.8, 1, 0.5, 1)
blgr.fg('blgr', 0.5, 1, 0.9, 1)
green.fg('green', 0, 0.4, 1, 1)
blue.fg('blue', 0.1, 0.3, 0.8, 1)
blood.fg('blood', 0.83, 0.39, 0.44, 1)
erro.fg('red', 1, 0.2, 0, 1)
cutoff.fg('white', 1, 1, 1, 1)
Roman.font('cmtt12', 'roman')
star1,star2,earth,sata=loader.loadTexture( path+'11211.jpg'),\
                        loader.loadTexture(path+'11511.jpg'),\
                        loader.loadTexture(path+'11311.jpg'),\
                        loader.loadTexture(path+'11411.jpg')
im = [earth, sata, star1, star2]

#some mess and their explanation
tip = ''  #str object for checking whether to give tips or not
Tip1, Tip2 = 1, 1  #tips
initTextObject, StartButton = 1, 1  #Welcom direct
StarMenu, StarMenucanvas = 1, 1  #Main menu and its canvas to move
size = (0, 0.996, -1.3, 1)  #Initial StarMenu['frameSize']
entryList, entryErroList = 1, 1  #While creating a card(temporary)
typeCard, typeframe = list(range(4)), list(range(4))  #4 types of stars
creatCard = 1  #Datas inquiry to create a card(once a time, usually destroied
sd = list('h' * 9)  #Datas(temporary)
StarCopy,mycard,MyStar,Cframe,ChArg,velo,posi=[],[],[],[],[],[],[]


#Stars' name ,card ,exactlly what the stars are,information card,
#argument to help see if the Cframe is open,
#velocity and position datas of all stars(Though they are just entries)
#main to import
class gui(ShowBase):
    def __init__(self):
        #self.quitMain()
        self.checkInit()
        self.Welcome()

    def quitMain(self):
        sys.exit()

    def Welcome(self):
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

    #base.buttonThrowers[0].node().setButtonDownEvent('anyButton')

    def checkInit(self):
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

    def begin(self):
        global world
        world = world.world()
        initTextObject.destroy()
        StartButton.destroy()
        if 'Tip1' in tip:
            pass
        else:
            self.Tip_1()
        self.OpenMenu()

    def Tip_1(self):
        global Tip1
        Tip1 = YesNoDialog(text=t_k1,
                           scale=1,
                           pos=(-0.02, 0, 0.22),
                           buttonTextList=['No tips', '\tNext'],
                           buttonValueList=[0, 1],
                           midPad=0.22,
                           button_relief=0,
                           relief=1,
                           command=self.Tip_2)

    def Tip_2(self, x):
        global Tip2
        if x:
            pass
        else:
            with open('res/config/Tips.csv', 'a') as tips:
                writer = csv.writer(tips)
                writer.writerow('Tip1')
        try:
            Tip1.destroy()
        except:
            pass
        if 'Tip2' in tip:
            pass
        else:
            Tip2 = YesNoCancelDialog(
                text=t_k2,
                scale=1,
                pos=(-0.02, 0, 0.22),
                buttonTextList=['No tips', '\tLast', 'Next'],
                buttonValueList=[0, -1, 1],
                midPad=0.22,
                button_relief=0,
                relief=1,
                command=self.tip_pau)

    def tip_pau(self, x):
        Tip2.destroy()
        if x == 0:
            with open('res/config/Tips.csv', 'a') as tips:
                writer = csv.writer(tips)
                writer.writerow('Tip2')
        elif x == -1:
            self.Tip_1()

    def OpenMenu(self):
        global StarMenu, StarMenucanvas
        global world
        try:
            world.takeMouseAway()
        except:
            pass
        StarMenu = DirectScrolledFrame(relief=0,
                                       frameSize=(0, 0.996, -1.1, 1),
                                       canvasSize=size,
                                       pos=(0.91, 0, 0),
                                       scrollBarWidth=0.04)

        StarMenucanvas = StarMenu.getCanvas()
        StarMenucanvasParent = StarMenucanvas.getParent()

        self.Species()
        Cut_off = geneFrame(StarMenucanvas, (0, 0.965, -0.02, 0),
                            (0, 0, -0.073), (0.5, 0.5, 0.5, 1), 2)
        cut_off = geneText(Cut_off.frame, '\1white\1.\2' * 42, 0.1,
                           (0.47, -0.011, 0))
        try:
            for ID in range(len(MyStar)):
                MyStar[ID].Card(0)
        except:
            pass

        base.win.getEngine().renderFrame()
        # Only calling DSF.guiItem.recompute() gives imprecise position.
        # DSF.guiItem.recompute()
        StarMenucanvasDefaultPos = StarMenucanvas.getPos()

        # Must know the canvas position range
        StarMenu['horizontalScroll_value'] = StarMenu[
            'verticalScroll_value'] = 1
        StarMenu.guiItem.recompute()
        StarMenucanvasRange = StarMenucanvasDefaultPos - StarMenucanvas.getPos(
        )
        StarMenucanvasRange[0] = abs(StarMenucanvasRange[0])
        StarMenucanvasRange[2] = abs(StarMenucanvasRange[2])
        StarMenu['horizontalScroll_value'] = StarMenu[
            'verticalScroll_value'] = 0

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
            StarMenu['horizontalScroll_value'] = -canvasPos[
                0] / StarMenucanvasRange[0]
            StarMenu[
                'verticalScroll_value'] = canvasPos[2] / StarMenucanvasRange[2]
            return task.cont

        base.accept('mouse1', startScroll)
        base.accept('q', self.closeMenu)

    def closeMenu(self):
        global StarMenu, size
        StarMenu.hide()
        base.accept('q', self.OpenMenu)

    def Species(self):
        global typeCard, typeframe
        typeText = [
            '\1light\1Planet\2', '\1light\1Satalite\2', '\1light\1Star One\2',
            '\1light\1Star Two\2'
        ]
        for i in range(4):
            typeframe[i] = DirectFrame(
                parent=StarMenucanvas,
                frameSize=(0, 0.955, -0.26, 0),
                pos=(0, 0, 1 - 0.27 * i),
                relief=1,
                frameTexture=path + '11' + str(i + 2) + '1.jpg',
                image_scale=0.25,
                #geom=,
                text=typeText[i],
                text_pos=(0.8, -0.23, 0),
                text_scale=0.05)
            typeCard[i] = DirectCheckButton(
                parent=typeframe[i],
                relief=0,
                boxRelief=1,
                boxImage=im[i],
                scale=0.128,
                pos=(0.264, 0, -0.13),
                command=self.creat,
                extraArgs=[i])  #i is the order of the type

    def creat(self, x, i, n=0, y=-1):
        global creatCard, entryList, entryErroList, sd
        try:
            creatCard.frame.destroy()
        except:
            pass
        sd = list('h' * 9)
        creatCard = geneFrame(StarMenu, (0, 0.8, -1, 1), (-2.84, 0, 0),
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
                entryList[le] = geneEntry(creatCard.frame, 0.063,
                                          (0.1, 0, 0.8), 8, 1, None, [le])
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
            pos=(0.56, 0, -0.69),
            relief=0,
            button_relief=0,
            command=self.closeE,
            extraArgs=[i, y, n])

    def closeE(self, x, i, y, n=0):
        global entryList, entryErroList, creatCard, MyStar, StarCopy, ChArg, Cframe, velo, posi, size, StarMenu
        dd = 1
        if x:
            sd[0] = entryList[0].entry.get()
            for le in range(1, len(sd)):
                sd[le] = entryList[le].entry.get()
                try:
                    sd[le] = int(sd[le])
                    entryErroList[le] = geneText(entryList[le].entry,
                                                 '\1roman\1\1green\1Yes!\2\2',
                                                 0.68, (0.8, -1, 0))
                except:
                    entryErroList[le] = geneText(entryList[le].entry,
                                                 '\1roman\1\1red\1wrong\2\2',
                                                 0.68, (0.8, -1, 0))
                if entryErroList[le].text[
                        'text'] == '\1roman\1\1red\1wrong\2\2':
                    dd = 0
                    continue
            if dd:
                if n:
                    mycard[y].destroy()
                    ty = MyStar[y].ty
                    del MyStar[y]
                    star = StarCard(sd[0], sd[1], sd[2], [sd[3], sd[4], sd[5]],
                                    [sd[6], sd[7], sd[8]], ty)
                    StarCopy[y] = star.name
                    MyStar.insert(y, star)
                    star.Card(0)
                    '''for star in MyStar:
                        creatobject(star.type,
                                     star.Im,
                                     myname=star.name,
                                     mass=star.mas,
                                     radius=star.rad,
                                     vel=star.vel,
                                     cor=star.pos)'''

                else:
                    '''creatobject(ty[i],
                                texture,
                                myname=sd[0],
                                mass=sd[1],
                                radius=sd[2],
                                vel=[sd[6],sd[7],sd[8]],
                                cor=[sd[3],sd[4],sd[5]])'''
                    if not sd[0]:
                        sd[0] = 'Hapy'
                    star = StarCard(sd[0], sd[1], sd[2], [sd[3], sd[4], sd[5]],
                                    [sd[6], sd[7], sd[8]], i)
                    MyStar.append(star)
                    StarCopy.append(star.name)
                    ChArg.append(0)
                    Cframe.append(1)
                    velo.append(1)
                    posi.append(1)
                    star.Card(0)
                    Length = StarMenu['canvasSize']
                    size = (0, 0.996, Length[2] - 1, 1)
                    StarMenu.destroy()
                    self.OpenMenu()
                creatCard.frame.destroy()

        else:
            creatCard.frame.destroy()


#generate some widgets
class geneText(gui):
    def __init__(self, parenT, texT, scalE, poS):
        self.text = OnscreenText(parent=parenT,
                                 text=texT,
                                 scale=scalE,
                                 pos=poS)


class geneFrame(gui):
    def __init__(self, parenT, size, pos, color, relieF):
        self.frame = DirectFrame(parent=parenT,
                                 frameSize=size,
                                 pos=pos,
                                 frameColor=color,
                                 relief=relieF)


class geneEntry(gui):
    def __init__(self, parenT, scalE, poS, widtH, relieF, commanD, extra):
        self.entry = DirectEntry(parent=parenT,
                                 scale=scalE,
                                 pos=poS,
                                 width=widtH,
                                 relief=relieF,
                                 command=commanD,
                                 extraArgs=extra)


class StarCard(gui):
    def __init__(self, name, mas, rad, pos, vel, ty):
        self.name = name
        self.mas = mas
        self.rad = rad
        self.pos = pos
        self.vel = vel
        self.ty = ty

    def Card(self, x):
        global mycard
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
        if para != len(MyStar) - 1:
            mycard[para] = card
        else:
            mycard.insert(para, card)
        mycard[para].reparentTo(StarMenucanvas)
        myCha = DirectCheckButton(parent=mycard[para],
                                  boxImage=im[mystyle],
                                  scale=0.174,
                                  pos=(0.378, 0, -0.174),
                                  relief=0,
                                  boxRelief=1,
                                  boxBorder=0,
                                  command=self.Change,
                                  extraArgs=[para, myvel, mypos])
        myMass = OnscreenText(parent=mycard[para],
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
            self.Change(1, para, (0, 0, 0), (0, 0, 0))  #data update

    def Change(self, x, y, v, p):
        global velo, posi, Cframe, mycard, ChArg, ListS, StarMenu
        ChArg[y] = -1
        for j in range(len(MyStar[y + 1:])):
            mycard[j + y + 1].destroy()
            b = ChArg[:j + y + 1].count(-1)
            MyStar[j + y + 1].Card(0.325 * b)
            if ChArg[j + y + 1] == -1:
                #TemStar_
                MyStar[j + y + 1].Change(1, j + y + 1, (0, 0, 0),
                                         (0, 0, 0))  #data update
                break
            else:
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
                         pos=(2.5, 1.7, 0),
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
                                     '\1blgr\1Change Args\2', '\1blgr\1Delet\2'
                                 ],
                                 button_scale=1.1,
                                 pos=(0.5, 0, -0.186),
                                 buttonValueList=[-1, 0, 1],
                                 command=self.closeChange,
                                 extraArgs=[y])
        #ListS=List
        #self.updating(y)

    def updating(self, y):
        global velo, posi, TemStars, a
        while ChArg[y] == -1:
            a = 1
            #TemStar=gui_data(y)
            #
            '''if 1==1:
                for i in range(3):
                    posi[y][i].enterText('{:' '>8}'.format(int(TemStar[i]))+'{:.3f}'.format(TemStar[i]-int(TemStar[i])))
                    velo[y][i].enterText('{:' '>8}'.format(int(TemStar[i+3]))+'{:.3f}'.format(TemStar[i+3]-int(TemStar[i+3])))
            else:
                NewStar=List
                NewData=DataList
                l=0
                while l<len(ListS):
                    if NewList[l]==ListS[l]:
                        l+=1
                    else:
                        del ListS[l]
                        del StarCopy[y]
                        del ChArg[y]
                        
                        MyStar[y].destroy()
                        mycard[y].destroy()
                        self.Review(y-1)
                for star in NewList:
                    if star in ListS:
                        pass
                    else:
                        ListS.append(star)
                        starS=StarCard(DataList)
                        MyStar.append(starS)
                        StarCopy.append(starS.name)
                        Cframe.append(1)
                        ChArg.append(0)
                        star.Card(0)'''
    def closeChange(self, x, y):
        global ChArg, MyStar, StarCopy, size
        if x == -1:
            Cframe[y].destroy()
            ChArg[y] = 0
            self.Review(y)
        elif x == 1:
            del StarCopy[y]
            del ChArg[y]

            del MyStar[y]
            mycard[y].destroy()
            del mycard[y]
            size = (0, 0.996, Length[2] + 1, 1)
            self.Review(y - 1)
            #Mem.reinitialize()
            #star been delet
            '''for star in MyStar:
                        creatobject(star.type,
                                     star.Im,
                                     myname=star.name,
                                     mass=star.mas,
                                     radius=star.rad,
                                     vel=star.vel,
                                     cor=star.pos)'''

        else:
            self.creat(1, MyStar[y].ty, n=1, y=y)

    def Review(self, y, n=0):
        global mycard
        for i in range(len(MyStar[y + 1:])):
            mycard[i + y + 1].destroy()
            b = ChArg[:i + y + 1].count(-1)
            MyStar[i + y + 1].Card(0.325 * b)
            if ChArg[i + y + 1] == -1:
                #TemStar_
                self.Change(1, i + y, (0, 0, 0), (0, 0, 0))  #data update
            else:
                pass


def gui_data(y):
    if switch:
        [i, j, k], [vi, vj, vk] = List[y].cor, List[y].vel
        return [i, j, k, vi, vj, vk]
    else:
        return None
