'''
@Author: Alicespace
@Date: 2019-12-16 11:13:54
@LastEditTime : 2019-12-21 15:46:09
'''
from direct.showbase.ShowBase import ShowBase
base = ShowBase()
from render import starGui, world
from direct.gui.OnscreenText import OnscreenText
'''starGui.gui()'''
a = world.world()
a.takeMouseBack()
base.run()
