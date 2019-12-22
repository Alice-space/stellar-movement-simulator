'''
@Author: Alicespace
@Date: 2019-12-16 11:13:54
@LastEditTime : 2019-12-22 20:20:02
'''
from direct.showbase.ShowBase import ShowBase
from render import starGui, world
from direct.gui.OnscreenText import OnscreenText

if __name__ == '__main__':
    base = ShowBase()
    starGui.gui()
    base.run()
