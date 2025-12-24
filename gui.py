import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import numpy as np
import matplotlib
matplotlib.use("qtagg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

def setCustomSize(x, width, height):
    sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(x.sizePolicy().hasHeightForWidth())
    x.setSizePolicy(sizePolicy)
    x.setMinimumSize(QtCore.QSize(width, height))
    x.setMaximumSize(QtCore.QSize(width, height))

def pi_multiple_formatter(x, pos):
    num = int(np.rint(2 * x / np.pi))
    if num % 2 == 0:
        return r'$%s\pi$' % (num // 2)
    else:
        return r'$\frac{%s}{2}\pi$' % (num)

class CustomMainWindow(QMainWindow):

    slider_val = 0
    a1 = b1 = c1 = a2 = b2 = c2 = 0

    coord_min = -5
    coord_max = 5

    third_circle = None
    m_line = None
    m_point = None

    m_min = -3
    m_max = 4

    curr_m = 0

    phase_min = 0
    phase_max = 2 * np.pi
    phase_xticks = np.linspace(phase_min, phase_max, 5)

    def __init__(self):

        super(CustomMainWindow, self).__init__()

        # Define the geometry of the main window
        self.setGeometry(300, 300, 1200, 800)
        self.setWindowTitle("Recitifer")

        # Create FRAME_A
        self.FRAME_A = QFrame(self)
        # self.FRAME_A.setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(210,210,235,255).name())
        self.LAYOUT_A = QGridLayout()
        self.FRAME_A.setLayout(self.LAYOUT_A)
        self.setCentralWidget(self.FRAME_A)

        # Place the zoom button
        self.left_gb = QGroupBox(self)

        self.dValidator = QtGui.QDoubleValidator(self)
        
        # L : inductor
        self.inductor_lbl = QLabel(self)
        self.inductor_lbl.setText("L [mH]")
        self.inductor_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.l_input = QLineEdit(self)
        self.l_input.setValidator(self.dValidator)

        # C : capacitor
        self.capacitor_lbl = QLabel(self)
        self.capacitor_lbl.setText("C [nF]")
        self.capacitor_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.c_input = QLineEdit(self)

        # R : capacitor
        self.resistor_lbl = QLabel(self)
        self.resistor_lbl.setText("R [ohm]")
        self.resistor_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.r_input = QLineEdit(self)

        # V_m : maximum voltage
        self.voltage_lbl = QLabel(self)
        self.voltage_lbl.setText("V_m [V]")
        self.voltage_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.v_input = QLineEdit(self)

        self.left_grid = QGridLayout()
        self.left_gb.setLayout(self.left_grid)
        self.left_grid.addWidget(self.inductor_lbl, 0, 0)
        self.left_grid.addWidget(self.l_input, 0, 1)
        self.left_grid.addWidget(self.capacitor_lbl, 1, 0)
        self.left_grid.addWidget(self.c_input, 1, 1)
        self.left_grid.addWidget(self.resistor_lbl, 2, 0)
        self.left_grid.addWidget(self.r_input, 2, 1)
        self.left_grid.addWidget(self.voltage_lbl, 3, 0)
        self.left_grid.addWidget(self.v_input, 3, 1)

        # Button
        self.goBtn = QPushButton(text = 'GO')
        self.goBtn.clicked.connect(self.buttonGo)
        self.left_grid.addWidget(self.goBtn, 4, 0, 1, 2)

        # Place the matplotlib figure
        self.fig = plt.Figure()

        self.V_ax = self.fig.add_subplot(3, 1, 1) # Voltage
        self.I_ax = self.fig.add_subplot(3, 1, 2) # Current through R
        self.Q_ax = self.fig.add_subplot(3, 1, 3) # Capacitor's charge

        self.V_ax.set_aspect('auto')
        self.I_ax.set_aspect('auto')
        self.Q_ax.set_aspect('auto')

        self.V_ax.set_xlim(self.phase_min, self.phase_max)
        self.V_ax.set_ylim(-150, 150)
        self.I_ax.set_xlim(self.phase_min, self.phase_max)
        self.I_ax.set_ylim(-150, 150)
        self.Q_ax.set_xlim(self.phase_min, self.phase_max)
        self.Q_ax.set_ylim(-150, 150)

        self.V_ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
        self.V_ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_multiple_formatter))
        self.I_ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
        self.I_ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_multiple_formatter))
        self.Q_ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
        self.Q_ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_multiple_formatter))

        self.fig.gca().set_aspect('equal', adjustable='box')
        self.myFig = FigureCanvas(self.fig)
        self.LAYOUT_A.addWidget(self.left_gb, 0, 0)
        self.LAYOUT_A.addWidget(self.myFig, 0, 1)
        self.LAYOUT_A.setColumnStretch(0, 1)
        self.LAYOUT_A.setColumnStretch(1, 4)

        self.show()
    
    def buttonGo(self):
        l_value = int(self.l_input.text())
        c_value = int(self.c_input.text())
        r_value = int(self.r_input.text())
        v_value = int(self.v_input.text())
        print(f'L  : {l_value} [mH]')
        print(f'C  : {c_value} [nF]')
        print(f'R  : {c_value} [ohm]')
        print(f'V_m: {c_value} [V]')

if __name__== '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('macOS'))
    myGUI = CustomMainWindow()


    sys.exit(app.exec_())
