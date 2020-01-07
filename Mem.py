import time
import copy

from collections import deque

""" This module is the database for the program. GUI will input data given by
the user. The module calculateloop will get data from here, calculate, and put
the data back in. The 3DWorld module will output data, in the process clearing
memory storage space.

    An important class is defined here. The class StellarObject has instances
of stellar objects. They have properties such as ID, mass, radius and objdata 
that are used for calculation. Data concerning the coordinates and velocities
are stored in objdata, which is a deque object (double-ended-queue). A very im
portant aspect of deques is that it can follow both the FIFO rule and the FILO
rule, making calculation and 3D world rendering much easier (one needs to pop
data from the end of the queue and the other the front). Properties like read
& write state are used as switches. They mark the state of the object (whether
it should be visible to the 3DWorld module(readstate) and to the calculateloop
module(writestate)). Properties like the objtype and texture are used to draw
the object. Other properties are trivial and are only used for small tweaks in
the program. (Except for the property order, which is discussed in the related
functions.)
    It has two methods, dataIN and dataOUT. The dataOUT method has a judge sta
tement embedded so that when one object runs out of data, all the states will
change automatically. The rest part of the method serves to transform the form
of the data into what the 3DWorld module recognizes.

    Most functions in the module deals with data input and output. They are us
ually called by other modules.

    The following acts as an example of how to call this module. The first part
deals with data input. (Notice that only function createobjects is called while
you inputs data, and not function deleteobject. If you want to delete a object,
you have to clear the database because all the formerly calculated data will be
of no use now that you changed the current circumstance. Then create the object
s that you don't want to delete. The module is written in this way mainly to sa
tisfy the demand that the memory usage should be limited. Thus all the output d
ata is automatically deleted from the database.) The second part deals with da
ta output.

    import MEM
    import calculateloop
    MEM.createobject(objtype = "starO", texture = None, 
                     mass = 100, radius = 5, cor = [0, 0, 0], vel = [0, 0, 0])
    MEM.createobject(objtype = "Eplanet", texture = None,  
                     mass = 10, radius = 1, cor = [200, 0, 0], vel = [0, 40, 0])
    
    calculateloop.loopjudge(length = 120)
    objs = MEM.getcurrentobjects()
    while True:
        calculateloop.loopjudge(length = 120)
        if MEM.triggerstate == False:
            for obj in objs:
                temp = obj.dataOUT()
                print(obj.ID, obj.order, temp)
            print("--------" * 5)
        else:
            MEM.triggerstate = False
            objs = MEM.getcurrentobjects()

    Or if you want to get a more visual result, try the following.

    import MEM
    import calculateloop
    MEM.createobject(objtype = "starO", texture = None, 
                     mass = 100, radius = 5, cor = [0, 0, 0], vel = [0, 0, 0])
    MEM.createobject(objtype = "Eplanet", texture = None,  
                     mass = 10, radius = 1, cor = [200, 0, 0], vel = [0, 40, 0])
    
    calculateloop.loopjudge(length=120)
    objs = MEM.getcurrentobjects()
    import turtle
    n = len(objs)
    turtles = [turtle.Turtle() for k in range(n)]
    for k in range(n):
        turtles[k].pu()
        turtles[k].setpos(objs[k].objdata[0][4: 6])
        turtles[k].pd()
    while True:
        calculateloop.loopjudge(length=120)
        if MEM.triggerstate is False:
            for k in range(n):
                temp = objs[k].dataOUT()
                turtles[k].setpos(temp[4:6])
        else:
            MEM.triggerstate = False
            objs = MEM.getcurrentobjects() """

__author__ = "邢景琦 1900011435"

objects, lennum, objnum, t0, totalorder, safetynum = [], 0, 0 - 1, 0, 0, 60

triggerstate, calculatestate = False, False

class StellarObject:

    ''' See the notes for the whole module. '''

    def __init__(self, m, r, ID, objtype, texture, objdata = [], order = 0, 
                     read = True, write = True, name = "Default", namels = []):
        self.ID = ID
        self.name = name
        self.namels = namels
        self.mass = m
        self.radius = r
        self.order = order
        self.switch = False
        self.temptime = objdata[0][0]
        self.objtype = objtype
        self.texture = texture

        ''' objtype falls in one of the four types "starO", "starG", "Jplanet"
and "Eplanet", representing O-type main sequence star, G-type main sequence st
ar, Jupiter-like planet and Earth-like planet. texture is the picture that will
be pasted to the surface of the star shown in the 3DWorld. '''

        self.texture2D = None
        self.readstate = read
        self.writestate = write
        self.vel = objdata[0][1: 4]
        self.cor = objdata[0][4: 7]
        self.objdata = deque(objdata)

        ''' objdata = [[t, vel, cor]] '''

    def dataIN(self, ls):
        self.objdata.append(ls)
        return None

    def dataOUT(self):
        if self.order != totalorder:
            if len(self.objdata) == 1:
                changestate(self.order)
                templs = self.objdata.popleft()
                tempt = templs[0]
                templs[0] = templs[0] - self.temptime
                self.temptime = tempt
                self.readstate = False
                objects.remove(self)
                return templs
            else:
                templs = self.objdata.popleft()
                self.vel = templs[1: 4]
                self.cor = templs[4: 7]
                tempt = templs[0]
                templs[0] = templs[0] - self.temptime
                self.temptime = tempt
                return templs
        else:
            if len(self.objdata) >= 1 + safetynum:
                templs = self.objdata.popleft()
                self.vel = templs[1: 4]
                self.cor = templs[4: 7]
                tempt = templs[0]
                templs[0] = templs[0] - self.temptime
                self.temptime = tempt
                return templs
            else:
                raise ValueError("Need more calculation")

def changestate(ordernum):

    ''' This function deals with the variable triggerstate which acts as a swit
ch and the variable totalorder. By setting triggerstate = True, whoever using t
he data from the database will know that some sort of emerging event has happen
ed and the user needs to get a new object list for further usage, while trigger
state = False means no emerging event happend. The use of order is discussed in
the function appendstate. '''
    
    global triggerstate
    triggerstate = True
    for obj in objects:
        if obj.order == ordernum:
            length = len(obj.objdata)
            if length != 0 and length != 1:
                obj.order = obj.order + 1
            else:
                pass
        else:
            pass
    ordernum = ordernum + 1
    for obj in objects:
        if obj.order == ordernum:
            obj.readstate = True
        else:
            pass
    return None

def appendstate():

    ''' This function deals with the variable totalorder. The property order is
used to deal with the problem of which part of data should be used. If an emerg
ing event happens, every surviving object will get a new order. Those with this
order but are hiding in the database will now come out as current objects on th
e screen. (Emerged objects are deleted so they go into hiding. Emerging objects
have a higher order than the objects they come from. They will join others when
all the data in the emerged objects is used up, and the functions changestate &
appendstate are called.) With this property, different parts of the data can be
separated. '''
    
    global totalorder
    totalorder = totalorder + 1
    return None

def createobject(objtype, texture, myname = "Default", ls = [], order = 0,
                          vel = [], cor = [], time = 0, mass = 0, radius = 0,
                          read = True, write = True):

    ''' This function creates a new object for writing data. It is called eith
er by the GUI module or by the calculateloop module during calculation. '''
    
    global objnum
    objnum = objnum + 1
    datalist = [[time] + vel + cor]
    obj = StellarObject(m = mass, r = radius, ID = objnum,
                              objtype = objtype, texture = texture, 
                              read = read, write = write, order = order,
                              name = myname, namels = ls, objdata = datalist)
    objects.append(obj)
    return None

def deleteobject(obj):

    ''' This function deletes an existing objects for writing data. It is only
called by the calculateloop module. '''
    
    obj.writestate = False
    if len(obj.objdata) == 0:
        obj.readstate = False
    else:
        pass
    return None

def getobjectsdata():

    ''' Get the final data of all objects to calculate. The list objectsdata is
in the form listed below. (A trivial function) '''

    """ objectsdata = [[ti, vxi, vyi, vzi, xi, yi, zi, mi]] """
    
    objectsdata = []
    for obj in objects:
        if obj.writestate == True:
            mydata = obj.objdata.pop()
            mylist = [obj.mass] + mydata[1: 7] + [mydata[0]]
            objectsdata.append(mylist)
        else:
            pass
    return objectsdata

def getobjects():

    ''' Get all objects to calculate. (A trivial function) '''
    
    templs = []
    for obj in objects:
        if obj.writestate == True:
            templs.append(obj)
        else:
            pass
    return templs

def getcurrentobjects():

    ''' Get all objects to draw the 3D world and to show the objects in the GUI
. (A trivial function) '''
    
    templs = []
    for obj in objects:
        if obj.readstate == True:
            templs.append(obj)
        else:
            pass
    return templs

def reinitialize():

    ''' This function reinitializes the database. Only called by the GUI modu
le. (A trivial function) '''
    
    while calculatestate == True:
        time.sleep(1)
    global lennum, t0, totalorder, triggerstate,objects
    lennum, t0, totalorder, triggerstate = 0, 0, 0, False
    temp = []
    for obj in objects:
        if obj.readstate == True:
            obj.writestate = True
            obj.order = 0
            obj.switch = None
            obj.temptime = 0
            obj.objdata = deque([[0] + obj.vel + obj.cor])
            temp.append(obj)
    objects = temp
    return None

def processcreate(objtype, texture, myname = "Default", ls = [], order = 0,
                           vel = [], cor = [], time = 0, mass = 0, radius = 0,
                           read = True, write = True):

    ''' This function creates stellar objects in the process of the program. On
ly be called by the GUI module. (A trivial function) '''
    
    global objnum
    objnum = objnum + 1
    datalist = [[time] + vel + cor]
    obj = StellarObject(m = mass, r = radius, ID = objnum,
                              objtype = objtype, texture = texture, 
                              read = read, write = write, order = order,
                              name = myname, namels = ls, objdata = datalist)
    objects.append(obj)
    return None

def processdelete(obj):

    ''' This function deletes stellar objects in the process of the program. On
ly be called by the GUI module. (A trivial function) '''
    

    objects.remove(obj)
    return None

def returnnum():

    ''' Return the length of the database. (A trivial function) '''
    
    global lennum
    try:
        lennum = max([len(obj.objdata) for obj in objects])
    except ValueError:
        lennum = 0
    return lennum
