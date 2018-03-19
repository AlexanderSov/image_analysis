import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from imageWork import *


class MainWindow(QMainWindow):

    def __init__(self, path_to_picture='mephi.png', left=50, top=50):
        super().__init__()
        self.title = "Анализ изображений"
        self.left = left
        self.top = top
        self.width = 1024
        self.height = 768
        self.path_to_picture = path_to_picture
        self.changed = False
        self.label = QLabel(self)
        self.pixmap = QPixmap(self.path_to_picture)
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.change_widget()

        toolbar = self.addToolBar('file')
        open_file = QAction('Открыть', self)
        fast = QAction('Быстрый', self)
        for_human = QAction('Чел.глаз', self)
        desaturation = QAction('Десатурация', self)
        gradation_min = QAction('Градация(min)', self)
        gradation_max = QAction('Градация(max)', self)
        ackv = QAction('Эквализация', self)
        bar_chart = QAction('Гистограмма', self)

        # обрабатываем сигналы
        open_file.triggered.connect(self.show_dialog)
        fast.triggered.connect(lambda: self.show_changed_picture(0))
        for_human.triggered.connect(lambda: self.show_changed_picture(1))
        desaturation.triggered.connect(lambda: self.show_changed_picture(2))
        gradation_min.triggered.connect(lambda: self.show_changed_picture(3))
        gradation_max.triggered.connect(lambda: self.show_changed_picture(4))
        ackv.triggered.connect(lambda x=self.changed:
                               self.show_bar_chart(x, ackv=1))
        bar_chart.triggered.connect(lambda x=self.changed:
                                    self.show_bar_chart(x))

        # добавляем в меню
        toolbar.addAction(open_file)
        toolbar.addAction(fast)
        toolbar.addAction(for_human)
        toolbar.addAction(desaturation)
        toolbar.addAction(gradation_min)
        toolbar.addAction(gradation_max)
        toolbar.addAction(ackv)
        toolbar.addAction(bar_chart)

        self.show()

    def change_widget(self):
        self.pixmap = QPixmap(self.path_to_picture)
        pixmap5 = self.pixmap.scaled(1024, 700)
        self.label.setPixmap(pixmap5)
        self.setCentralWidget(self.label)
        self.resize(pixmap5.width(), pixmap5.height())


    def show_dialog(self):
        self.path_to_picture = QFileDialog.getOpenFileName(
            None, 'Open file', '/home')[0]
        self.change_widget()

    def show_changed_picture(self, mode):
        a = ImageTransform(self.path_to_picture)
        a.transform_picture(mode=mode)
        SecondWindow(a.path_new)

    def show_bar_chart(self, changed, ackv=0):
        a = ImageTransform(self.path_to_picture)
        a.make_bar_chart(self.changed, ackv)
        SecondWindow(a.path_new)


class SecondWindow(MainWindow):
    def __init__(self, path_to_picture):
        super().__init__(path_to_picture, 100, 100)
        self.changed = True


if __name__ == '__main__':
    app = QApplication(sys.argv)  # создает объект приложения, можно обратиться
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__),
                        'mephi.png')
    app.setWindowIcon(QIcon(path))
    main_window = MainWindow()
    sys.exit(app.exec_())
