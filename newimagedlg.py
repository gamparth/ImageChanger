#good code bro
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import ui_newimagedlg
class NewImageDlg(QDialog,ui_newimagedlg.Ui_ImageChooserDlg):
    def __init__(self,parent=None):
        super(NewImageDlg, self).__init__(parent)
        self.setupUi(self)
        self.color = Qt.red

        for value, text in (
                (Qt.SolidPattern, "Solid"),
                (Qt.Dense1Pattern, "Dense #1"),
                (Qt.Dense2Pattern, "Dense #2"),
                (Qt.Dense3Pattern, "Dense #3"),
                (Qt.Dense4Pattern, "Dense #4"),
                (Qt.Dense5Pattern, "Dense #5"),
                (Qt.Dense6Pattern, "Dense #6"),
                (Qt.Dense7Pattern, "Dense #7"),
                (Qt.HorPattern, "Horizontal"),
                (Qt.VerPattern, "Vertical"),
                (Qt.CrossPattern, "Cross"),
                (Qt.BDiagPattern, "Backward Diagonal"),
                (Qt.FDiagPattern, "Forward Diagonal"),
                (Qt.DiagCrossPattern, "Diagonal Cross")):
            self.brushComboBox.addItem(text,value)

        self.colorButton.clicked.connect(self.getColor)
        self.brushComboBox.activated.connect(self.setColor)
        self.setColor()
        self.spinBoxWidth.setFocus()

#aur kya chal rha hai munshii
    def getColor(self):
        color = QColorDialog.getColor(Qt.black,self)
        if color.isValid():
            self.color = color
            self.setColor()

    def image(self):
        pixmap = self._makepixmap(self.spinBoxWidth.value(),self.spinBoxHeight.value())
        return  QPixmap.toImage(pixmap)

    def setColor(self):
        pixmap = self._makepixmap(60,30)
        self.colorLabel.setPixmap(pixmap)

    def _makepixmap(self,width,height):
        pixmap = QPixmap(width, height)
        style = int(self.brushComboBox.itemData(self.brushComboBox.currentIndex()))
        brush = QBrush(self.color,Qt.BrushStyle(style))
        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(),Qt.white)
        painter.fillRect(pixmap.rect(),brush)
        return pixmap

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = NewImageDlg()
    form.show()
    app.exec_()
