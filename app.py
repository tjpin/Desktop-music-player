from threading import Thread
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import schedule
import sys
import ntpath
from mutagen.mp3 import MP3
from pygame import mixer

from PyQt5.uic import loadUiType

ui,_ = loadUiType("player.ui")


class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        mixer.init()

        self.callbacks()

    def update_buttons(self):
        self.actionFile.triggered.connect(self.select_files)
        self.pushButton_3.clicked.connect(self.play_track)
        self.pushButton_5.clicked.connect(self.pause_track)
        self.pushButton_6.clicked.connect(self.stop_track)
        self.dial.valueChanged.connect(self.volume_control)
        self.horizontalSlider.valueChanged.connect(self.forward_slider)
        self.progressBar.setValue(mixer.music.get_pos())

    def callbacks(self):
        self.update_buttons()

    def select_files(self):
        global filename
        filename = QFileDialog.getOpenFileName()[0]
        self.load_tracks()
        self.get_duration()
        return filename

    def load_tracks(self):
        self.get_current()

    def play_track(self):
        music = filename
        try:
            paused
        except:
            mixer.music.load(music)
            mixer.music.play()
        mixer.music.unpause()

    def pause_track(self):
        global paused
        paused = True
        mixer.music.pause()

    def continue_Play(self):
        self.play_track()

    def stop_track(self):
        mixer.music.stop()

    def get_current(self):
        active = filename
        _, n = ntpath.split(active)
        self.setWindowTitle(f"Playing {n}")
        self.label_3.setText(n)

    def repeat_one(self):
        pass

    def shuffle_tracks(self):
        pass

    def search_track(self):
        pass

    def get_duration(self):
        def converter(seconds):
            h = seconds // 3600
            seconds %= 3600
            min = seconds // 60
            seconds %= 60
            return h, min, seconds
        tag = MP3(filename)
        global data
        data = tag.info.length
        hours, mins, sec = converter(data)
        duration = f"{round(hours)}:{round(mins)}:{round(sec)}"
        self.label_4.setText(duration)

    def volume_control(self, value):
        volume = int(value) / 100
        mixer.music.set_volume(volume)

    def forward_slider(self, value):
        mixer.music.set_pos(float(value) * data / 100)

    def play_previous(self):
        pass

    def play_next(self):
        pass

    def settings(self):
        pass

    def help(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    tr = Thread(target=main)
    tr.start()