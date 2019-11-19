'''
@Author: Alicespace
@Date: 2019-11-18 08:06:30
@LastEditTime: 2019-11-19 12:01:27
'''

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile


class stellarMovementSimulator(ShowBase):
    def __init__(self):
        loadPrcFile("res/config/Config.prc")
        ShowBase.__init__(self)
        # self.scene = self.loader.loadModel("res/tmp/earth/earth")


app = stellarMovementSimulator()
app.run()
