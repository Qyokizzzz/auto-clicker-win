import keyboard
import threading
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QLabel, QSpinBox, QDoubleSpinBox, QPushButton, QRadioButton, \
    QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QCheckBox
from src.AutoClicker import AutoClicker
from src.Utils import sleep

class DZAutoClickerUI(QMainWindow):

    def __init__(self):
        super().__init__()

        # area1
        self.repeat_key_label = QLabel('重复按键:',self)
        self.repeat_key_input = QLineEdit('mouseLeft', self)
        self.repeat_key_input.setFixedWidth(80)
        repeat_key_hbox = QHBoxLayout()
        repeat_key_hbox.addWidget(self.repeat_key_label, 1)
        repeat_key_hbox.addWidget(self.repeat_key_input, 1)

        self.click_type_label = QLabel('点击类型:', self)
        self.click_type_input = QComboBox(self)
        self.click_type_input.setFixedWidth(80)
        self.click_type_input.addItems(['单击', '双击', '按住'])
        self.click_type_input.activated.connect(self.handle_click_type_change)
        click_type_hbox = QHBoxLayout()
        click_type_hbox.addWidget(self.click_type_label, 1)
        click_type_hbox.addWidget(self.click_type_input, 1)

        vbox1 = QVBoxLayout()
        vbox1.addLayout(repeat_key_hbox)
        vbox1.addLayout(click_type_hbox)
        vbox1.setGeometry(QtCore.QRect(50, 20, 150, 80))
        self.setLayout(vbox1)


        # area2
        self.interval_label = QLabel('间隔:', self)
        self.interval_input = QDoubleSpinBox(self)
        self.interval_input.setFixedWidth(80)
        interval_hbox = QHBoxLayout()
        interval_hbox.addWidget(self.interval_label, 1)
        interval_hbox.addWidget(self.interval_input, 1)

        self.duration_label = QLabel('按住时长:', self)
        self.duration_input = QDoubleSpinBox(self)
        self.duration_input.setFixedWidth(80)
        self.duration_input.setEnabled(False)
        duration_hbox = QHBoxLayout()
        duration_hbox.addWidget(self.duration_label, 1)
        duration_hbox.addWidget(self.duration_input, 1)

        vbox2 = QVBoxLayout()
        vbox2.addLayout(interval_hbox)
        vbox2.addLayout(duration_hbox)
        vbox2.setGeometry(QtCore.QRect(250, 20, 150, 80))
        self.setLayout(vbox2)


        # area3
        self.cur_pos_checkbox = QCheckBox('自定义位置', self)
        self.cur_pos_checkbox.stateChanged.connect(self.handle_cur_pos_changed)

        self.hotkey_label = QLabel('热键', self)
        self.hotkey_input = QLineEdit('f4', self)
        self.hotkey_input.setFixedWidth(80)
        hotkey_hbox = QHBoxLayout()
        hotkey_hbox.addWidget(self.hotkey_label, 1)
        hotkey_hbox.addWidget(self.hotkey_input, 1)

        area3 = QVBoxLayout()
        area3.addLayout(hotkey_hbox)
        area3.addWidget(self.cur_pos_checkbox)
        area3.setGeometry(QtCore.QRect(50, 120, 150, 80))
        self.setLayout(area3)


        # area4
        self.x_label = QLabel('横坐标:',self)
        self.x_input = QLineEdit(self)
        self.x_input.setFixedWidth(80)
        self.x_input.setEnabled(False)
        x_hbox = QHBoxLayout()
        x_hbox.addWidget(self.x_label, 1)
        x_hbox.addWidget(self.x_input, 1)

        self.y_label = QLabel('纵坐标:', self)
        self.y_input = QLineEdit(self)
        self.y_input.setFixedWidth(80)
        self.y_input.setEnabled(False)
        y_hbox = QHBoxLayout()
        y_hbox.addWidget(self.y_label, 1)
        y_hbox.addWidget(self.y_input, 1)

        cur_pos_vbox = QVBoxLayout()
        cur_pos_vbox.addLayout(x_hbox)
        cur_pos_vbox.addLayout(y_hbox)
        cur_pos_vbox.setGeometry(QtCore.QRect(250, 120, 150, 80))
        self.setLayout(cur_pos_vbox)


        # area5
        self.repeat_until_stop_radio = QRadioButton('重复到结束', self)
        self.repeat_until_stop_radio.setChecked(True)
        self.repeat_until_stop_radio.toggled.connect(self.handle_repeat_type_change)

        self.repeat_times_radio = QRadioButton('重复次数', self)
        self.repeat_times_radio.toggled.connect(self.handle_repeat_type_change)

        self.repeat_times_input = QSpinBox(self)
        self.repeat_times_input.setFixedWidth(80)
        self.repeat_times_input.setEnabled(False)
        self.repeat_times_label = QLabel('次', self)

        repeat_hbox = QHBoxLayout()
        repeat_hbox.addWidget(self.repeat_until_stop_radio, 6)
        repeat_hbox.addWidget(self.repeat_times_radio, 3)
        repeat_hbox.addWidget(self.repeat_times_input, 2)
        repeat_hbox.addSpacing(5)
        repeat_hbox.addWidget(self.repeat_times_label, 1)

        repeat_hbox.setGeometry(QtCore.QRect(50, 220, 385, 30))
        self.setLayout(repeat_hbox)

        self.confirm_button = QPushButton('确定', self)
        self.confirm_button.clicked.connect(self.handle_confirm)
        self.pause_button = QPushButton('停止', self)
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.handle_pause)

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.confirm_button, 1)
        btn_hbox.addWidget(self.pause_button, 1)
        btn_hbox.setGeometry(QtCore.QRect(50, 280, 350, 30))
        self.setLayout(btn_hbox)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('每次修改配置前需要停止当前监听')

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('DZ Auto Clicker')
        self.show()

        self.clicker = None
        self.thread = None
        self.listening = False
        self.click_type = 0

    def handle_click_type_change(self, activated):
        self.click_type = activated
        self.duration_input.setEnabled(activated == 2)

    def handle_cur_pos_changed(self, state):
        self.x_input.setEnabled(state)
        self.y_input.setEnabled(state)

    def handle_repeat_type_change(self):
        self.repeat_times_input.setEnabled(self.repeat_times_radio.isChecked())

    def handle_confirm(self):
        self.freeze()
        self.init_clicker()
        self.listening = True
        self.thread = threading.Thread(target=self.add_hotkey_listener)
        self.thread.daemon = True
        self.thread.start()

    def handle_pause(self):
        self.listening = False
        if self.thread is not None:
            self.thread.join(timeout=1)
            self.thread = None
        self.recover()

    def add_hotkey_listener(self):
        clicker = self.clicker
        if not clicker:
            return

        while self.listening:
            if keyboard.is_pressed(clicker.hotkey):
                clicker.trigger = not clicker.trigger

                if clicker.trigger:
                    clicker.start()
                else:
                    clicker.stop()

                sleep(1)

    def freeze(self):
        self.confirm_button.setEnabled(False)
        self.pause_button.setEnabled(True)

        self.repeat_key_input.setEnabled(False)
        self.interval_input.setEnabled(False)
        self.click_type_input.setEnabled(False)
        self.hotkey_input.setEnabled(False)
        self.cur_pos_checkbox.setEnabled(False)
        self.repeat_until_stop_radio.setEnabled(False)
        self.repeat_times_input.setEnabled(False)

        self.duration_input.setEnabled(False)
        self.x_input.setEnabled(False)
        self.y_input.setEnabled(False)
        self.repeat_times_input.setEnabled(False)

    def recover(self):
        self.confirm_button.setEnabled(True)
        self.pause_button.setEnabled(False)

        self.repeat_key_input.setEnabled(True)
        self.interval_input.setEnabled(True)
        self.click_type_input.setEnabled(True)
        self.hotkey_input.setEnabled(True)
        self.cur_pos_checkbox.setEnabled(True)
        self.repeat_until_stop_radio.setEnabled(True)
        self.repeat_times_input.setEnabled(True)

        self.duration_input.setEnabled(self.click_type_input.currentIndex() == 2)
        self.x_input.setEnabled(self.cur_pos_checkbox.isChecked())
        self.y_input.setEnabled(self.cur_pos_checkbox.isChecked())
        self.repeat_times_input.setEnabled(self.repeat_times_radio.isChecked())

    def init_clicker(self):
        repeat_key = self.repeat_key_input.text()
        click_type = self.click_type
        interval = int(self.interval_input.value())
        duration = int(self.duration_input.value())
        hotkey = self.hotkey_input.text()

        x = None
        y = None
        if self.cur_pos_checkbox.isChecked():
            x = int(self.x_input.text())
            y = int(self.y_input.text())

        times = None
        if self.repeat_times_radio.isChecked():
            times = self.repeat_times_input.value()

        self.clicker = AutoClicker(repeat_key, click_type, interval, duration, hotkey, x, y, times)
