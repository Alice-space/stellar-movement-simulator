from collections import deque
"""
needs
getobjects() -> objls
getobjectsdata() -> objdatals
obj.objdata -> [[t, vel, cor]]
createobject()
deleteobject()
"""

objects, lennum, objnum, t0, totalorder, safetynum = [], 0, 0 - 1, 0, 0, 60

triggerstate, resetworld = False, False


class StellarObject:
    def __init__(self,
                 m,
                 r,
                 ID,
                 objtype,
                 texture,
                 objdata=[],
                 order=0,
                 read=True,
                 write=True,
                 name="Default",
                 namels=[]):
        self.ID = ID
        self.name = name
        self.namels = namels
        self.mass = m
        self.radius = r
        self.order = order
        self.objtype = objtype
        self.texture = texture
        self.readstate = read
        self.writestate = write
        self.temptime = objdata[0][0]
        self.objdata = deque(objdata)

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
                return templs
            else:
                templs = self.objdata.popleft()
                tempt = templs[0]
                templs[0] = templs[0] - self.temptime
                self.temptime = tempt
                return templs
        else:
            if len(self.objdata) >= 1 + safetynum:
                templs = self.objdata.popleft()
                tempt = templs[0]
                templs[0] = templs[0] - self.temptime
                self.temptime = tempt
                return templs
            else:
                raise ValueError("Need more calculation")


def changestate(ordernum):
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
    global totalorder
    totalorder = totalorder + 1
    return None


def createobject(objtype,
                 texture,
                 myname="Default",
                 mass=0,
                 radius=0,
                 vel=[],
                 cor=[],
                 time=0,
                 ls=[],
                 order=0,
                 read=True,
                 write=True):
    global objnum
    objnum = objnum + 1
    datalist = [[time] + vel + cor]
    obj = StellarObject(m=mass,
                        r=radius,
                        ID=objnum,
                        objtype=objtype,
                        texture=texture,
                        objdata=datalist,
                        order=order,
                        read=read,
                        write=write,
                        name=myname,
                        namels=ls)
    objects.append(obj)
    return None


def deleteobject(obj):
    obj.writestate = False
    return None


def getobjectsdata():
    objectsdata = []
    for obj in objects:
        if obj.writestate == True:
            mydata = obj.objdata.pop()
            mylist = [obj.mass] + mydata[1:7] + [mydata[0]]
            objectsdata.append(mylist)
        else:
            pass
    return objectsdata


def getobjects():
    templs = []
    for obj in objects:
        if obj.writestate == True:
            templs.append(obj)
        else:
            pass
    return templs


def getcurrentobjects():
    templs = []
    for obj in objects:
        if obj.readstate == True:
            templs.append(obj)
        else:
            pass
    return templs


def reinitialize():
    global resetworld, objects, lennum, objnum, t0, totalorder
    resetworld = True
    objects, lennum, objnum, t0, totalorder = [], 0, 0 - 1, 0, 0
    return None


def returnnum():
    global lennum
    lennum = max([len(obj.objdata) for obj in objects])
    return lennum
