import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

# Interpret image data as row-major instead of col-major
pg.setConfigOptions(imageAxisOrder='row-major')

app = QtGui.QApplication([])

## Create window with ImageView widget
win = QtGui.QMainWindow()
win.resize(800,800)
imv = pg.ImageView()
win.setCentralWidget(imv)
win.show()

chaos = np.array([[64., 46., 53., 44.],
                 [36., 33., 22., 34.],
                 [29., 21., 32., 43.],
                 [45., 36., 28., 33.]])

imv.setImage(chaos, levels=(0, 255))

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
