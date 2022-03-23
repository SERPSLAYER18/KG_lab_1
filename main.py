import sys

import numpy as np
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout
)

from controllers import (
    LabeledHSlider,
    RGBController,
    XYZController,
    MasterController,
    CMYKController
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 300
        self.top = 300
        self.width = 800
        self.height = 300
        self.title = 'Color app'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setAutoFillBackground(True)
        p = self.palette()
        init_color = np.array([100, 100, 200])
        p.setColor(self.backgroundRole(), QColor(*init_color))
        self.setPalette(p)

        main_layout = QVBoxLayout()
        sliders = QHBoxLayout()

        r = LabeledHSlider('Red')
        g = LabeledHSlider('Green')
        b = LabeledHSlider('Blue')
        sliders.addLayout(r)
        sliders.addLayout(g)
        sliders.addLayout(b)
        rgb_controller = RGBController([r, g, b])

        x = LabeledHSlider('X')
        y = LabeledHSlider('Y')
        z = LabeledHSlider('Z')
        sliders.addLayout(x)
        sliders.addLayout(y)
        sliders.addLayout(z)
        xyz_controller = XYZController([x, y, z])

        c = LabeledHSlider('C')
        m = LabeledHSlider('M')
        y = LabeledHSlider('Y')
        k = LabeledHSlider('K')
        sliders.addLayout(c)
        sliders.addLayout(m)
        sliders.addLayout(y)
        sliders.addLayout(k)
        cmyk_controller = CMYKController([c, m, y, k])

        rgb_controller.set_rgb(init_color)
        xyz_controller.set_rgb(init_color)
        cmyk_controller.set_rgb(init_color)

        master = MasterController([rgb_controller, xyz_controller, cmyk_controller], self)

        main_layout.addLayout(sliders)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()