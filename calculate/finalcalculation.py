from scipy.integrate import solve_ivp
from calculate import Mem
""" objectlist = [[mass, vx0, vy0, vz0, x0, y0, z0, t0]]"""
""" globals = [objectID, objectlist, objectdata, n, y0, sol, t0] """

G, C, judgedistance = 10000, 300000000, 10

objectID, objectlist, data, n, y0, sol, t0 = [], [], [], 0, [], None, 0

delta_t = Mem.returnt()


def calculate(delta_t=delta_t):

    # initialize the problem
    def initialize():
        global objectID, objectlist, n, t0, y0
        objectID = Mem.getobjects()
        objectlist = Mem.getobjectsdata()
        n = len(objectlist)
        for k in range(n):
            y0.extend(objectlist[k][1:7])
        t0 = objectlist[0][7]
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
        global sol
        sol = solve_ivp(solution, t_span=[t0, t0 + delta_t], y0=y0)
        """ sol.t = [ti]
            sol.y = [[variablei(ti) for ti in t] for variables in y]"""
        return None

    def tempdata():
        trange = len(sol.t)
        for objnum in range(n):
            templs = []
            for tsep in range(trange):
                templs.append([
                    sol.t[tsep], sol.y[objnum * 6 + 0][tsep],
                    sol.y[objnum * 6 + 1][tsep], sol.y[objnum * 6 + 2][tsep],
                    sol.y[objnum * 6 + 3][tsep], sol.y[objnum * 6 + 4][tsep],
                    sol.y[objnum * 6 + 5][tsep]
                ])
            data.append(templs)
        return None

    def judge():
        criticalpoint = None
        for t in range(len(sol.t)):
            judgelist = []
            for objnum in range(n):
                myjudgelist = [objnum]
                for sep in [k for k in range(n) if k > objnum]:
                    d = ((data[sep][t][3] - data[objnum][t][3])**(2) +
                         (data[sep][t][4] - data[objnum][t][4])**(2) +
                         (data[sep][t][5] - data[objnum][t][5])**(2))**(1 / 2)
                    if d <= judgedistance:
                        myjudgelist.append(sep)
                    else:
                        pass
                if len(myjudgelist) == 1:
                    pass
                else:
                    judgelist.append(myjudgelist)
            if len(judgelist) != 0:
                criticalpoint = t
                break
            else:
                pass
        if criticalpoint is None:
            return ["not in collision course"]
        else:
            return ["in collision course", judgelist, criticalpoint]

    def savedata():
        judgement = judge()
        if judgement[0] == "not in collision course":
            pass
        elif judgement[0] == "in collision course":
            criticalpoint = judgement[2]
            for objnum in range(n):
                data[objnum] = data[objnum][0:criticalpoint + 1]
            for emergels in judgement[1]:
                m, vells, corls = 0, [0, 0, 0], [0, 0, 0]
                for objnum in emergels:
                    objdata = data[objnum].pop()
                    m = m + objectID[objnum].mass
                    vells[0] = vells[0] + objdata[1]
                    vells[1] = vells[1] + objdata[2]
                    vells[2] = vells[2] + objdata[3]
                    corls[0] = corls[0] + objdata[4]
                    corls[1] = corls[1] + objdata[5]
                    corls[2] = corls[2] + objdata[6]
                Mem.createobject(myname="Default",
                                 mass=m,
                                 time=criticalpoint,
                                 vel=vells,
                                 cor=corls)
                for num in emergels:
                    Mem.deleteobject(objectID[num])
            for objnum in range(n):
                templs = data[objnum]
                for k in range(len(templs)):
                    objectID[objnum].dataIN(templs[k])
            global t0
            t0 = sol.t[criticalpoint]
        return None

    # initialize
    initialize()
    # solve data
    solve()
    # handle data
    tempdata()
    savedata()

    return None


def loopcalculate(length=100):
    while Mem.returnnum() <= length:
        calculate()
    return None
