import sys
from PySide6 import QtCore, QtWidgets, QtGui
from google_api import get_google_df
from eve_api import get_system_DF
from pandas import DataFrame


notrent = '#13a10e'
aval = '#c2760c'
notaval = '#a30506'
noval = '#cccccc'
bg = '#323335'
strc = '#a4a4a4'
bgb = '#64676a'

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.on_top = False
        self.can_move = True
        self.err = False

        self.setWindowIcon(QtGui.QIcon('appico.ico'))
        self.setWindowTitle('ECR')

        # Размеры
        self.resize(300, 120)
        self.setFixedSize(300,120)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        # Основные кнопки
        self.b_exet = QtWidgets.QPushButton("X")
        self.b_hide = QtWidgets.QPushButton("-")

        # Дополнительные кнопки
        #self.b_language = QtWidgets.QPushButton('L')
        self.b_upper = QtWidgets.QPushButton('U')
        self.b_stop_move = QtWidgets.QPushButton('S')

        # Фиксируем размер кнопок
        self.b_exet.setFixedSize(25,25)
        self.b_hide.setFixedSize(25,25)
        #self.b_language.setFixedSize(25,25)
        self.b_upper.setFixedSize(25,25)
        self.b_stop_move.setFixedSize(25,25)

        # Поиск системы
        # self.b_find = QtWidgets.QPushButton('Find')
        # self.b_find.setFixedSize(75,35)

        # ВВод текста
        self.text_area = QtWidgets.QTextEdit()
        self.text_area.setFixedSize(290,25)
        self.text_area.textChanged.connect(self.find_system)
        self.text_output = QtWidgets.QLabel()
        self.text_output.setFixedSize(290, 40)

        # Выравнивание
        self.l_main = QtWidgets.QVBoxLayout()
        self.l_top_b = QtWidgets.QHBoxLayout()
        self.l_bottom_b = QtWidgets.QHBoxLayout()

        self.l_main.setContentsMargins(3,3,3,3)
        self.l_top_b.setContentsMargins(3,3,3,3)
        self.l_bottom_b.setContentsMargins(3,3,3,3)

        # Добавляем кнопки
        self.topBL = [self.b_exet, self.b_hide, self.b_upper, self.b_stop_move]
        #self.l_top_b.addWidget(self.b_language, 0, QtCore.Qt.AlignLeft)
        self.l_top_b.addWidget(self.b_upper, 0, QtCore.Qt.AlignLeft)
        self.l_top_b.addWidget(self.b_stop_move, 0, QtCore.Qt.AlignLeft)
        self.l_top_b.addWidget(QtWidgets.QLabel(), 1, QtCore.Qt.AlignCenter)
        self.l_top_b.addWidget(self.b_hide, 0, QtCore.Qt.AlignRight)
        self.l_top_b.addWidget(self.b_exet, 0, QtCore.Qt.AlignRight)

        # Нижние кнопки
        self.l_bottom_b.addWidget(self.text_area)
        # self.l_bottom_b.addWidget(self.b_find)

        # Добавляем все в главный виджет
        self.l_main.addLayout(self.l_top_b, 0)
        self.l_main.addWidget(self.text_output)
        self.l_main.addLayout(self.l_bottom_b, 0)
        self.setLayout(self.l_main)

        # Подключаем кнопки
        self.b_exet.clicked.connect(self.close_app)
        self.b_hide.clicked.connect(self.hide_app)

        #self.b_language.clicked.connect(self.change_lang)
        self.b_upper.clicked.connect(self.set_upper)
        self.b_stop_move.clicked.connect(self.stop_move)


        # self.b_find.clicked.connect(self.find_system)

        # Делаем кнопки красивыми
        for i in self.topBL:
            i.setStyleSheet(f"background-color: {bg};"
                            "border-width: 3px;"
                            f"border-color: {bgb};"
                            "border-radius: 5px;"
                            "border-style: outset;"
                            f"color: {strc};"
                            "font-weight: 900"
                            )

        # self.b_find.setStyleSheet(f"background-color: {bg};"
        #                             "border-width: 3px;"
        #                             f"border-color: {bgb};"
        #                             "border-radius: 5px;"
        #                             "border-style: outset;"
        #                             f"color: {strc};"
        #                             "font-weight: 900"
        #                             )

        self.text_area.setStyleSheet(f"background-color: {bgb};"
                                    f"border-color: {bgb};"
                                    "border-width: 5px;"
                                    "border-radius: 10%;"
                                    )

        self.setStyleSheet(f"background-color: {bg};"
                            )

        self.loading()

    @QtCore.Slot()
    def close_app(self):
        self.close()

    @QtCore.Slot()
    def hide_app(self):
        self.showMinimized()

    @QtCore.Slot()
    def change_lang(self):
        pass

    @QtCore.Slot()
    def set_upper(self):
        self.on_top = not self.on_top
        print(self.on_top)
        if self.on_top:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.show()

    @QtCore.Slot()
    def stop_move(self):
        self.can_move = not self.can_move

    @QtCore.Slot()
    def find_system(self):
        syst = str(self.text_area.toPlainText())
        if syst[0] == '<':
            try:
                b = syst.split('<')
                syst = b[1].split('>')[1]
            except Exception:
                self.text_output.setText('Wrong input!')
        try:
            syst = syst.upper()
            syst = syst.replace('*', '')
            syst = syst.replace(' ', '')
            syst = syst.replace('\t', '')
            syst = syst.replace('\n', '')
        except:
            self.text_output.setText('Wrong input!')

        if any(self.all_systems['name'].isin([syst])):
            if syst in self.systems_in_renta.index:
                if self.systems_in_renta.loc[syst, 'Availability'] == 'Yes':
                    self.text_output.setText('  System ' + syst + ' is available, but in RENT LIST')
                    self.text_output.setStyleSheet(f"background-color: {aval};"
                                                    f"border-color: {aval};"
                                                    "border-width: 5px;"
                                                    "border-radius: 10%;"
                                                    "font-weight: 900"
                                                    )
                else:
                    self.text_output.setText('  System ' + syst + ' NOT available in RENT LIST')
                    self.text_output.setStyleSheet(f"background-color: {notaval};"
                                                    f"border-color: {notaval};"
                                                    "border-width: 5px;"
                                                    "border-radius: 10%;"
                                                    "font-weight: 900"
                                                    )
            else:
                self.text_output.setText('  System ' + syst + ' is NOT in RENT LIST')
                self.text_output.setStyleSheet(f"background-color: {notrent};"
                                                    f"border-color: {notrent};"
                                                    "border-width: 5px;"
                                                    "border-radius: 10%;"
                                                    "font-weight: 900"
                                                    )
        else:
            self.text_output.setText('  System ' + syst + ' DOESN\'T EXIST or\n  NOT in my Data Base! Check input!')
            self.text_output.setStyleSheet(f"background-color: {bgb};"
                                                    f"border-color: {bgb};"
                                                    "border-width: 5px;"
                                                    "border-radius: 10%;"
                                                    "font-weight: 900"
                                                    )

    def loading(self):
        # Get Google data
        self.systems_in_renta = get_google_df()
        text = ''
        if isinstance(self.systems_in_renta, DataFrame):
            text += 'Data from Google   RECEIVED\n'
        else:
            text += 'Data from Google   ERROR\n'
            self.err = True
        self.text_output.setText(text)

        # Get EVE data
        self.all_systems = get_system_DF()
        if isinstance(self.all_systems, DataFrame):
            text += 'Data from EVE        RECEIVED\n'
        else:
            text += 'Data from EVE        Error\n'
            self.err = True
        self.text_output.setText(text)


    def mousePressEvent(self, event):
        if self.can_move:
            if event.button() == QtCore.Qt.LeftButton:
                self.offset = event.pos()
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.can_move:
            if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.pos() - self.offset)
            else:
                super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.can_move:
            self.offset = None
            super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())