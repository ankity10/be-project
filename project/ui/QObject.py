import sys
from PyQt4.QtCore import QObject, pyqtSignal  # really shouldn't import * here...QtCore library is quite large
from PyQt4.QtGui import QPushButton, QVBoxLayout, QDialog, QApplication 

class TestView(QDialog):
    request = pyqtSignal()

    def __init__(self, parent=None):
        super(TestView, self).__init__(parent)
        self.button = QPushButton('Click')
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        self.request.emit()

class TestController(QObject):
    def __init__(self, view):
        super(QObject, self).__init__()
        self.view = view
        self.view.request.connect(self.respond)

    def respond(self):

        print 'respond'

app = QApplication(sys.argv)
dialog = TestView()
controller = TestController(dialog)
dialog.show()
app.exec_()
