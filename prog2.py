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
        self.matrix_size = 3
        self.matrix = None

        self.label = QLabel(self)
        self.pixmap = QPixmap(self.path_to_picture)
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.change_widget()

        toolbar = self.addToolBar('file')
        open_file = QAction('Открыть', self)
        matrix_size = QAction('Задать размер матрицы', self)
        matrix_elements = QAction('Задать элементы', self)
        matrix_apply = QAction('Приментить', self)

        open_file.triggered.connect(lambda: self.show_dialog(0))
        matrix_size.triggered.connect(lambda: self.show_dialog(1))
        matrix_elements.triggered.connect(lambda: self.show_dialog(2))
        matrix_apply.triggered.connect(self.apply_matrix)

        toolbar.addAction(open_file)
        toolbar.addAction(matrix_size)
        toolbar.addAction(matrix_elements)
        toolbar.addAction(matrix_apply)

        self.show()

    def change_widget(self):
        self.pixmap = QPixmap(self.path_to_picture)
        self.label.setPixmap(self.pixmap)
        self.setCentralWidget(self.label)
        self.resize(self.pixmap.width(), self.pixmap.height())

    def show_dialog(self, mode):
        """ mode:
            0 - get path to the picture
            1 - get matrix size
        """
        if mode == 0:
            self.path_to_picture = QFileDialog.getOpenFileName(
                None, 'Open file', '/home')[0]
            self.change_widget()
        elif mode == 1:
            self.matrix_size = QInputDialog.getInt(self,
                                                   'Размер матрицы',
                                                   'Введите целое число:')[0]
            print(self.matrix_size)
        elif mode == 2:
            table = MyTableDialog(matrix_size=self.matrix_size)

    def apply_matrix(self, ):
        a = ImageTransform(self.path_to_picture)
        a.apply_matrix(self.matrix_size, self.matrix)
        SecondWindow(a.path_new)


class SecondWindow(MainWindow):
    def __init__(self, path_to_picture):
        super().__init__(path_to_picture, 100, 100)
        self.changed = True


class MyTableDialog(MainWindow):
    def __init__(self, matrix_size=3):
        super().__init__()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setGeometry(400, 400, 400, 400)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        self.table = QTableView(self)

        grid_layout.addWidget(self.table)
        self.model = QStandardItemModel(matrix_size, matrix_size)
        self.table.setModel(self.model)

        button = QPushButton("Сохранить")
        grid_layout.addWidget(button)
        button.clicked.connect(self.save_values)

        self.show()

    def save_values(self):
        model = self.table.model()
        data = []
        for row in range(model.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                data[row].append(int(model.data(index)))
        main_window.matrix = data


if __name__ == '__main__':
    app = QApplication(sys.argv)
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__),
                        'mephi.png')
    app.setWindowIcon(QIcon(path))
    main_window = MainWindow()
    sys.exit(app.exec_())
