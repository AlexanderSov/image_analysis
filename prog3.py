import sys

from PyQt5.QtWidgets import *


class ArithCoding:

    def __init__(self, phrase='eaii!', alphabet='aeiou!', num='0.23354'):
        self.phrase = phrase
        self.alphabet = alphabet
        list_ver1 = [1 / len(self.alphabet) for i in range(len(self.alphabet))]
        list_ver1.insert(0, 0)
        self.list_ver = list_ver1  # [0, 0.2, 0.3, 0.1, 0.2, 0.1, 0.1]

        self.interval = float(num)  # [0.23354, 0.2336]
        self.decode_phrase = ''
        self.decode_phrase_s = None

    def do_coding(self):
        """
        new_high = old_low + (old_high - old_low) * high_range(x)
        new_low = old_low + (old_high - old_low) * low_range(x)
        где old_low и old_high - границы интервала в котором представляется
        текущий символ
        highRange(x) и lowRange(x) - исходные границы кодируемого символа
        """
        old_low = 0
        old_high = 1
        for i in range(len(self.phrase)):
            index = self.alphabet.index(self.phrase[i])
            new_high = old_low + (old_high - old_low) * sum(self.list_ver[:index+2])
            new_low = old_low + (old_high - old_low) * sum(self.list_ver[:index+1])
            old_low = new_low
            old_high = new_high
        self.interval = str(old_low) + ';' + str(old_high)

    def do_decoding(self):
        """
        code - текущее значение кода,
        code_n = (code - low_range(x)) / (high_range(x) - low_range(x))
        """
        symbol = ''
        code = self.interval
        list_ver_sum = [sum(self.list_ver[:i+1]) for i in range(len(self.list_ver))]
        while symbol != '!':
            for i in range(len(list_ver_sum)):
                if list_ver_sum[i] <= code:
                    pass
                else:
                    symbol = self.alphabet[i - 1]
                    self.decode_phrase += symbol
                    # self.decode_phrase.append(symbol)
                    index = i
                    break
            code_n = (code - list_ver_sum[index - 1]) / (
                        list_ver_sum[index] - list_ver_sum[index - 1])
            code = code_n


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        self.e1 = QLineEdit()
        self.e2 = QLineEdit()
        self.e3 = QLineEdit()
        self.e4 = QLineEdit()
        self.e5 = QLineEdit()

        self.btn1 = QPushButton("Введите словарь")
        self.btn2 = QPushButton("Введите фразу")
        self.btn4 = QPushButton("Введите последовательность")

        self.flo = QFormLayout()
        self.initUI()

        self.alphabet = None
        self.phrase = None

    def initUI(self):

        self.e3.setFixedWidth(200)

        self.btn1.clicked.connect(lambda: self.get_text(0))
        self.btn2.clicked.connect(lambda: self.get_text(1))
        self.btn4.clicked.connect(lambda: self.get_text(2))

        self.flo.addRow(self.btn1, self.e1)
        self.flo.addRow(self.btn2, self.e2)
        self.flo.addRow("Результат кодировки", self.e3)
        self.flo.addRow(self.btn4, self.e4)
        self.flo.addRow("Результат декодировки", self.e5)

        self.widget.setLayout(self.flo)
        self.widget.setWindowTitle("Лабораторная 3")
        self.widget.show()

    def get_text(self, mode=0):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Введите последовательность')
        if ok and mode == 0:
            self.e1.setText(str(text))
            self.alphabet = text
        elif ok and mode == 1:
            self.e2.setText(str(text))
            self.phrase = text
            a = ArithCoding(phrase=self.phrase, alphabet=self.alphabet)
            a.do_coding()
            self.e3.setText(a.interval)
        elif ok and mode == 2:
            self.e4.setText(str(text))
            a = ArithCoding(alphabet=self.alphabet, num=text)
            a.do_decoding()
            self.e5.setText(a.decode_phrase)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
