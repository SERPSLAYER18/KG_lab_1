from typing import List

import numpy as np
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QLabel,
    QSlider,
    QVBoxLayout,
    QWidget
)


class LabeledHSlider(QVBoxLayout):

    def __init__(self, text, minimum=0, maximum=255):
        super().__init__()
        self.label = QLabel(text)
        self.slider = QSlider()
        self.addWidget(self.slider)
        self.addWidget(self.label)
        self.setLabelColor((255, 255, 255))
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)

    def value(self) -> int:
        return self.slider.value()

    def setValue(self, a0: int) -> None:
        self.slider.setValue(a0)

    def setLabelColor(self, rgb):
        p = self.label.palette()
        p.setColor(self.label.foregroundRole(), QColor(*rgb))
        self.label.setPalette(p)

    def lock_update(self):
        self.slider.blockSignals(True)

    def unlock_update(self):
        self.slider.blockSignals(False)


class ColorController():

    def __init__(self, rgb_sliders: List[LabeledHSlider], values: np.array = np.array([0, 0, 0])):
        self.master = None
        self.sliders = rgb_sliders

    def set_sliders_values(self, values):
        for value, slider in zip(values, self.sliders):
            slider.setValue(value)

    def get_sliders_values(self):
        values = []
        for slider in self.sliders:
            values.append(slider.value())
        return np.array(values)

    def get_rgb(self):
        raise NotImplementedError
        pass

    def set_rgb(self, rgb):
        raise NotImplementedError
        pass

    def update(self):
        self.master.controller_updated(self)
        pass

    def lock_signals(self):
        for slider in self.sliders:
            slider.lock_update()

    def unlock_signals(self):
        for slider in self.sliders:
            slider.unlock_update()

    def set_master(self, master):
        self.master = master
        for slider in self.sliders:
            slider.slider.valueChanged.connect(self.update)


class RGBController(ColorController):
    def get_rgb(self):
        return self.get_sliders_values()

    def set_rgb(self, rgb):
        self.set_sliders_values(rgb)


class XYZController(ColorController):

    def get_rgb(self):
        return np.clip(XYZ2RGB(self.get_sliders_values() / 255) * 255, 0, 255).astype(np.int32)

    def set_rgb(self, rgb):
        xyz = np.clip(RGB2XYZ(rgb / 255) * 255, 0, 255).astype(np.int32)
        self.set_sliders_values(xyz)


class CMYKController(ColorController):

    def get_rgb(self):
        return np.clip(CMYK2RGB(self.get_sliders_values() / 255) * 255, 0, 255).astype(np.int32)

    def set_rgb(self, rgb):
        xyz = np.clip(RGB2CMYK(rgb / 255) * 255, 0, 255).astype(np.int32)
        self.set_sliders_values(xyz)


class MasterController:
    def __init__(self, color_controllers: List[ColorController], to_be_painted: QWidget):
        self.controllers = color_controllers
        self.to_be_painted = to_be_painted
        for controller in self.controllers:
            controller.set_master(self)

    def controller_updated(self, controller: ColorController):
        rgb = controller.get_rgb()
        for other_controller in self.controllers:
            if not other_controller == controller:
                other_controller.lock_signals()
                other_controller.set_rgb(rgb)
                other_controller.unlock_signals()

        p = self.to_be_painted.palette()
        p.setColor(self.to_be_painted.backgroundRole(), QColor(*rgb))
        self.to_be_painted.setPalette(p)


##################################################
#               sRGB color system                #
##################################################
GAMMA = 2.2

M_RGB2XYZ = [[0.4124564, 0.3575761, 0.1804375],
             [0.2126729, 0.7151522, 0.0721750],
             [0.0193339, 0.1191920, 0.9503041]]

M_XYZ2RGB = np.linalg.inv(M_RGB2XYZ)


##################################################


def XYZ2RGB(xyz):
    rgb = np.clip(np.dot(M_XYZ2RGB, xyz), 0, 1)
    RGB = np.clip(np.power(rgb, 1 / GAMMA), 0, 1)
    # print(xyz, RGB)
    return RGB


def RGB2XYZ(rgb):
    v = np.float_power(rgb, GAMMA)
    XYZ = np.clip(np.dot(M_RGB2XYZ, v), 0, 1)
    return XYZ


def RGB2CMYK(rgb):
    K = 1 - max(rgb)
    K = np.clip(K,0.001, 1 - 0.001)
    CMY = (1 - rgb - K) / (1 - K)
    CMYK = np.clip([*CMY, K], 0, 1)
    return CMYK


def CMYK2RGB(cmyk):
    K = cmyk[-1]
    CMY = cmyk[:-1]
    rgb = (1 - CMY) * (1 - K)
    rgb = np.clip(rgb, 0, 1)
    return rgb


if __name__ == '__main__':
    print("Module launched")
else:
    print("Imported module " + __name__)
