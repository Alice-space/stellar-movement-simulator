from scipy.integrate import solve_ivp
from calculate import Mem
""" objectlist = [[mass, vx0, vy0, vz0, x0, y0, z0, t0]] """
""" globals = [objects, objectlist, tdata, ydata, tlist, n, y0, sol, t0] """

G, C = 10000, 300000000

Default_Texture = 'res/tmp/earth/earth.egg'

objects, objectlist, tdata, ydata, y0, sol, n = [], [], [], [], [], None, 0

t0, delta_t, tlist = 0, 10, []


# initialize the problem
def initialize():
    global objects, objectlist, n, t0, y0, tdata, ydata, criticalpoint
    objects = Mem.getobjects()
    objectlist = Mem.getobjectsdata()
    n = len(objectlist)
    y0 = []
    for k in range(n):
        y0.extend(objectlist[k][1:7])
    t0 = objectlist[0][7]
    tdata, ydata, sol = [], [], None
    return None


# transform the problem into a set of equations
def solution(t, y):
    """ y = [dxidt, dyidt, dzidt, xi, yi, zi] """
    def force(num):
        xforce = 0
        yforce = 0
        zforce = 0
        for k in range(n):
            if k != num:
                cor = [
                    y[6 * k + 3] - y[6 * num + 3],
                    y[6 * k + 4] - y[6 * num + 4],
                    y[6 * k + 5] - y[6 * num + 5]
                ]
                sqd = cor[0]**2 + cor[1]**2 + cor[2]**2
                tempm = objectlist[k][0]
                xforce = xforce + tempm * cor[0] / (sqd**(3 / 2))
                yforce = yforce + tempm * cor[1] / (sqd**(3 / 2))
                zforce = zforce + tempm * cor[2] / (sqd**(3 / 2))
            else:
                pass
        return [xforce * G, yforce * G, zforce * G]

    returnlist = []
    for loop in range(n):
        tempforce = force(loop)
        extendlist = [
            tempforce[0], tempforce[1], tempforce[2], y[6 * loop + 0],
            y[6 * loop + 1], y[6 * loop + 2]
        ]
        returnlist.extend(extendlist)
    return returnlist


# solve the set of equations
def solve():
    global sol, tdata, ydata, tlist
    sol = solve_ivp(solution, t_span=[t0, t0 + delta_t], y0=y0)
    """ sol.t = [ti]
        sol.y = [[variablei(ti) for ti in t] for variables in y]"""
    tdata = sol.t
    ydata = sol.y
    tlist = []
    return None


def stepjudge():
    global tlist
    temptsep = len(tlist)
    try:
        tempt = tdata[temptsep]
    except IndexError:
        return "need data"
    tlist.append(tempt)
    vel, cor = [], []
    for num in range(n):
        vel.append([
            sol.y[num * 6 + 0][temptsep], sol.y[num * 6 + 1][temptsep],
            sol.y[num * 6 + 2][temptsep]
        ])
        cor.append([
            sol.y[num * 6 + 3][temptsep], sol.y[num * 6 + 4][temptsep],
            sol.y[num * 6 + 5][temptsep]
        ])
    judgeset = set()
    for num in range(n):
        if num not in judgeset:
            myjudgelist = [num]
            for sep in [k for k in range(n) if k != num and k not in judgeset]:
                d = ((cor[sep][0] - cor[num][0])**(2) +
                     (cor[sep][1] - cor[num][1])**(2) +
                     (cor[sep][2] - cor[num][2])**(2))**(1 / 2)
                judgedistance = (objects[sep].radius + objects[num].radius)
                if objects[sep].objtype != "star" and objects[num] != "star":
                    pass
                else:
                    judgedistance = judgedistance / 2
                if d <= judgedistance:
                    myjudgelist.append(sep)
                    judgeset.add(sep)
                    judgeset.add(num)
                else:
                    pass
            if myjudgelist != [num]:
                m, r, V, mvells, mcorls = 0, 0, 0, [0, 0, 0], [0, 0, 0]
                tempnamels = []
                temptypeset = set()
                for objnum in myjudgelist:
                    mymass = objects[objnum].mass
                    mvells[0] = mvells[0] + vel[objnum][0] * mymass
                    mvells[1] = mvells[1] + vel[objnum][1] * mymass
                    mvells[2] = mvells[2] + vel[objnum][2] * mymass
                    mcorls[0] = mcorls[0] + cor[objnum][0] * mymass
                    mcorls[1] = mcorls[1] + cor[objnum][1] * mymass
                    mcorls[2] = mcorls[2] + cor[objnum][2] * mymass
                    m = m + mymass
                    V = V + objects[objnum].radius**3
                    tempnamels.append(objects[objnum].name)
                    temptypeset.add(objects[objnum].objtype)
                    Mem.deleteobject(objects[objnum])
                temporder = Mem.totalorder + 1
                r = V**(1 / 3)
                vells = [mvells[0] / m, mvells[1] / m, mvells[2] / m]
                corls = [mcorls[0] / m, mcorls[1] / m, mcorls[2] / m]
                temptype = None
                if "star" in temptypeset:
                    temptype = "star"
                elif "Jplanet" in temptypeset:
                    temptype = "Jplanet"
                elif "Eplanet" in temptypeset:
                    temptype = "Eplanet"
                else:
                    pass
                Mem.createobject(objtype=temptype,
                                 texture=Default_Texture,
                                 myname="Default",
                                 mass=m,
                                 radius=r,
                                 read=False,
                                 write=True,
                                 time=tempt,
                                 ls=tempnamels,
                                 order=temporder,
                                 vel=vells,
                                 cor=corls)
            else:
                pass
        else:
            pass
    if judgeset == set():
        for objnum in [k for k in range(n)]:
            templs = [tempt] + vel[objnum] + cor[objnum]
            objects[objnum].dataIN(templs)
        return True
    else:
        Mem.appendstate()
        for objnum in [k for k in range(n) if k not in judgeset]:
            templs = [tempt] + vel[objnum] + cor[objnum]
            objects[objnum].dataIN(templs)
        return False


def loopjudge(length=120):
    initialize()
    solve()
    while Mem.returnnum() <= length:
        verdict = stepjudge()
        if verdict is True:
            pass
        elif verdict is False:
            initialize()
            solve()
        elif verdict == "need data":
            initialize()
            solve()
    return None
