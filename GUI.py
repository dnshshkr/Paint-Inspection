import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QWidget, QSlider


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_pos:int=3
        self.current_pos:int=0
        self.setWindowTitle('Settings')
        self.resize(300,250)
        self.label=QLabel(self)
        self.label.move(130,100)
        self.slider=QSlider(Qt.Orientation.Horizontal,self)
        self.slider.setGeometry(50,50,200,50)
        self.slider.setRange(3,9)
        self.slider.setSingleStep(2)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(2)
        self.slider.sliderMoved.connect(self.sliderStep)
        self.slider.valueChanged.connect(self.display)
        self.slider.valueChanged.connect(self.lastStep)
        self.label.setText(str(self.slider.value()))
        self.label.adjustSize()

    def lastStep(self):
        self.last_pos=self.sender().value()
        pass
    
    def sliderStep(self):
        print(self.current_pos,self.last_pos)
        # if self.slider.value()%2!=0:
        #     if self.slider.sliderMoved(self.slider.value()>last_pos):
        #         self.slider.setValue(self.slider.value()+1)
        #     if self.slider.sliderMoved(self.slider.value()<last_pos):
        #         self.slider.setValue(self.slider.value()-1)

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())
    
    def display(self):
        #print(self.sender().value())
        self.current_pos=self.sender().value()
        print(self.last_pos)
        self.label.setText(str(self.sender().value()))
        self.label.adjustSize()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())