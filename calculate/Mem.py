from collections import deque
"""
needs
getobjects() -> objls
getobjectsdata() -> objdatals
obj.objdata -> [[t, vel, cor]]
createobject()
deleteobject()
"""

objects, num, t0, delta_t = [], 0, 0, 1


class StellarObject:
    def __init__(self, m, objdata=[]):
        self.mass = m
        self.ID = self
        self.state = "survive"
        self.objdata = deque(objdata)

    def dataIN(self, ls):
        self.objdata.append(ls)
        return None

    def dataOUT(self):
        try:
            templs = self.objdata.popleft()
            return templs
        except:
            return "run out of data"


def createobject(myname="Default", mass=0, vel=[], cor=[], time=0):
    mylist = [[time] + vel + cor]
    obj = StellarObject(m=mass, objdata=mylist)
    objects.append(obj)
    return None


def deleteobject(ID):
    ID.state = "destroy"
    return None


def getobjectsdata():
    objectsdata = []
    for obj in objects:
        if obj.state == "survive":
            mydata = obj.objdata.pop()
            mylist = [obj.mass] + mydata[1:7] + [mydata[0]]
            objectsdata.append(mylist)
    return objectsdata


def getobjects():
    templs = [obj for obj in objects if obj.state == "survive"]
    return templs


def returnnum():
    global num
    num = max([len(obj.objdata) for obj in objects])
    return num


def returnt():
    return delta_t
