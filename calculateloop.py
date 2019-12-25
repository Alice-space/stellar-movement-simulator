import Mem as MEM

from scipy.integrate import solve_ivp

""" This module deals with the calculation of the coordinates and velocities 
of different stellar objects at different points of time.

The main part of the calculation is done using scipy.integrate, and the rest 
of this module deals with data input and output while judging whether stellar
objects have collided with each other and change the database accordingly.

The current calculation algorithm is the Runge-Kutta45 method embedded in the 
scipy module, but we will try to write the Runge-Kutta algorithm ourselves as
well as adding other algorithms like the Verlet algorithm and the Forest-Ruth
algorithm which are symplectic, which means they conform to the basic laws of
momentun and angular momentum conservation in physics. 

The data flow in the program is discussed thoroughly in the MEM module, which
serves as the database of the program. """

__author__ = "邢景琦 1900011435"

""" objectlist = [[mass, vx0, vy0, vz0, x0, y0, z0, t0]] """

""" globals = [objects, objectlist, tdata, ydata, tlist, n, y0, sol, t0] """

G, C = 10000 / 3, 300000000

objects, objectlist, tdata, ydata, y0, sol, n = [], [], [], [], [], None, 0

t0, delta_t, tlist, tempt = 0, 0.1, [], 0

# initialize the problem
def initialize():
    
    ''' This function initializes the calculation progress. The list objects
contains all the stellar objects that need to be calculated. The list object
list contains all the data of the corresponding stellar objects in the form
shown under __author__. The list y0 is the initial value of the equation that
needs to be solved. '''
    
    global objects, objectlist, n, t0, y0, tdata, ydata
    objects = MEM.getobjects()
    objectlist = MEM.getobjectsdata()
    n = len(objectlist)
    emergetweak(objectlist)
    objects = MEM.getobjects()
    objectlist = MEM.getobjectsdata()
    n = len(objectlist)
    y0 = []
    for k in range(n):
        y0.extend(objectlist[k][1: 7])
    t0 = objectlist[0][7]
    tdata, ydata = [], []
    return None

def emergetweak(datals):

    ''' This function judges whether initial objects are overlapping with each
other and auto-emerges the overlapping stellar objects. '''
    
    vel, cor = [], []
    for ls in datals:
        vel.append(ls[1: 4])
        cor.append(ls[4: 7])
    del datals
    judge(vel, cor, neworder = False)
    return None

# transform the problem into a set of equations
def solution(t, y):

    ''' This standarlizes the differential equation that the scipy module will
calculate. The argument y is in the form listed below. It is written wholly to
call the function in the scipy module. (A trivial function) '''
    
    """ y = [dxidt, dyidt, dzidt, xi, yi, zi] """
    
    def force(num):
        xforce = 0
        yforce = 0
        zforce = 0
        for k in range(n):
            if k != num:
                cor = [y[6 * k + 3] - y[6 * num + 3],
                       y[6 * k + 4] - y[6 * num + 4],
                       y[6 * k + 5] - y[6 * num + 5]]
                sqd = cor[0] ** 2 + cor[1] ** 2 + cor[2] ** 2
                tempm = objectlist[k][0]
                xforce = xforce + tempm * cor[0]/(sqd ** (3/2))
                yforce = yforce + tempm * cor[1]/(sqd ** (3/2))
                zforce = zforce + tempm * cor[2]/(sqd ** (3/2))
            else:
                pass
        return [xforce * G, yforce * G, zforce * G]
    returnlist = []
    for loop in range(n):
        tempforce = force(loop)
        extendlist = [tempforce[0], tempforce[1], tempforce[2],
                      y[6 * loop + 0], y[6 * loop + 1], y[6 * loop + 2]]
        returnlist.extend(extendlist)
    return returnlist

# solve the set of equations
def solve():

    ''' This function calls the solve_ivp function in the scipy module to get
the result of the calculation. The return value sol has the attributives t and
y in the form listed below. (A trivial function) '''
    
    global sol, tdata, ydata, tlist
    sol = solve_ivp(solution, t_span = [t0, t0 + delta_t], y0 = y0)
    
    """ sol.t = [ti]
        sol.y = [[variablei(ti) for ti in t] for variables in y]"""
    
    tdata = sol.t
    ydata = sol.y
    tlist = []
    return None

def removeduplicate(ls):

    ''' This function removes extra items in a list if the same item occurs for
more than once. (A trivial funcction) '''
    
    templs = []
    for item in ls:
        if item in templs:
            pass
        else:
            templs.append(item)
    return templs

def integrate(judgelist):

    ''' This function judges if two sets in a list are overlapping and emerge
those that overlaps. To call this function, use the while statement until the
return value of emergestate is False. '''
    
    emergestate = False
    integratedjudgelist = []
    for myset in judgelist:
        integratedset = myset
        for otherset in judgelist:
            if myset == otherset:
                pass
            else:
                if integratedset.intersection(otherset) != set():
                    integratedset = integratedset.union(otherset)
                    emergestate = True
                else:
                    pass
        integratedjudgelist.append(integratedset)
    integratedjudgelist = removeduplicate(integratedjudgelist)
    return [emergestate, integratedjudgelist]

def judge(vel, cor, neworder):

    ''' This function judges whether the objects are overlapping at a specifi
ed time using vel and cor corresponding to the objects in the global argument
objects. Then it will append the data to the database or delete old objects &
create new objects and append their data to the database.

    The neworder parameter exists so that the function can be called under two
circumstances. One is in the initializing part where you do not want to get a
new object that has a higher order than current order. (See notes in MEM) The
other is the judgement done to the calculated data to see if it is appropriate
to append it to the database, where you do want such thing to happen. (See the
same notes in MEM) '''

    # judge
    judgelist = []
    emergingobjects = set()
    for num in range(n):
        myjudgeset = set()
        for sep in [k for k in range(n) if k != num]:
            d = ( (cor[sep][0] - cor[num][0]) ** (2) 
                + (cor[sep][1] - cor[num][1]) ** (2) 
                + (cor[sep][2] - cor[num][2]) ** (2)) ** (1 / 2)
            judgedistance = (objects[sep].radius + objects[num].radius)
            if d <= judgedistance:
                myjudgeset.add(sep)
                myjudgeset.add(num)
                emergingobjects.add(sep)
                emergingobjects.add(num)
            else:
                pass
        if len(myjudgeset) != 0:
            judgelist.append(myjudgeset)
        else:
            pass
    # change objects
    if judgelist != []:
        judgelist = removeduplicate(judgelist)
        loopstate = True
        while loopstate == True:
            judgement, templs = integrate(judgelist)
            loopstate = judgement
            judgelist = templs
            
        ''' The following part deletes the objects that are to be emerged and
creates new emerged objects. '''
        
        for myjudgeset in judgelist:
            m, r, V, mvells, mcorls = 0, 0, 0, [0, 0, 0], [0, 0, 0]
            tempnamels = []
            temptypeset = set()
            for objnum in myjudgeset:
                mymass = objects[objnum].mass
                mvells[0] = mvells[0] + vel[objnum][0] * mymass
                mvells[1] = mvells[1] + vel[objnum][1] * mymass
                mvells[2] = mvells[2] + vel[objnum][2] * mymass
                mcorls[0] = mcorls[0] + cor[objnum][0] * mymass
                mcorls[1] = mcorls[1] + cor[objnum][1] * mymass
                mcorls[2] = mcorls[2] + cor[objnum][2] * mymass
                m = m + mymass
                V = V + objects[objnum].radius ** 3
                if objects[objnum].name == "Default":
                    tempnamels.append(objects[objnum].name)
                else:
                    tempnamels.extend(objects[objnum].namels)
                temptypeset.add(objects[objnum].objtype)
                MEM.deleteobject(objects[objnum])
            temporder = MEM.totalorder
            r = V ** (1 / 3)
            vells = [mvells[0] / m, mvells[1] / m, mvells[2] / m]
            corls = [mcorls[0] / m, mcorls[1] / m, mcorls[2] / m]
            temptype = None
            if "starO" in temptypeset:
                temptype = "starO"
            elif "starG" in temptypeset:
                temptype = "starG"
            elif "Jplanet" in temptypeset:
                temptype = "Jplanet"
            elif "Eplanet" in temptypeset:
                temptype = "Eplanet"
            else:
                raise ValueError("Stellar object type can only be one in \
                                          starO, starG, Jplanet and Eplanet")
            if neworder == True:
                temporder = temporder + 1
                read = False
                write = True
            else:
                read = True
                write = True
            MEM.createobject(objtype = temptype, texture = None, time = tempt,
                             mass = m, radius = r, read = read, write = write,
                             myname = "Default", ls = tempnamels,
                             order = temporder, vel = vells, cor = corls)
    else:
        pass
    # append data to the database
    if judgelist == []:
        for objnum in [k for k in range(n)]:
            templs = [tempt] + vel[objnum] + cor[objnum]
            objects[objnum].dataIN(templs)
        return True
    else:
        if neworder == True:
            MEM.appendstate()
        else:
            pass
        for objnum in [k for k in range(n)
                               if k not in emergingobjects]:
            templs = [tempt] + vel[objnum] + cor[objnum]
            objects[objnum].dataIN(templs)
        return False

def stepjudge():

    ''' This function judges whether calculated data are appropriate to go to
the database. It calls the function judge to do the job. '''
    
    global tlist, tempt
    temptsep = len(tlist)
    try:
        tempt = tdata[temptsep]
    except IndexError:
        return "need data"
    tlist.append(tempt)
    vel, cor = [], []
    for num in range(n):
        vel.append([sol.y[num * 6 + 0][temptsep],
                    sol.y[num * 6 + 1][temptsep],
                    sol.y[num * 6 + 2][temptsep]])
        cor.append([sol.y[num * 6 + 3][temptsep],
                    sol.y[num * 6 + 4][temptsep],
                    sol.y[num * 6 + 5][temptsep]])
    judgement = judge(vel, cor, neworder = True)
    return judgement

def loopjudge(length = 120):

    ''' This function will enter a loop which calculates and judges again and
again until the database has enough data for 3D drawing. The length of the da
ta in the database can be specified using the parameter length. '''

    MEM.calculatestate = True
    if MEM.returnnum() > length:
        pass
    else:
        initialize()
        solve()
        while MEM.returnnum() <= length:
            verdict = stepjudge()
            if verdict == True:
                pass
            elif verdict == False:
                initialize()
                solve()
            elif verdict == "need data":
                initialize()
                solve()
    MEM.calculatestate = False
    return None
