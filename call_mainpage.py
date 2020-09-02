from PyQt5 import QtCore, QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QApplication, QFileDialog
from TelloUserInterface import Ui_Form
from Tello_Drone import *
import sys
from os import walk
import time


# TODO(JZQ): 在Plotter中添加重置视角的button
# TODO(JZQ): 增加TAG标签的隐藏选项
# TODO(JZQ): 增加保存文件、导入文件、导入音乐功能
# TODO(JZQ): 增加显示音乐波形的功能


class MainPageWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainPageWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.comobox_init()
        self.music_play_init()
        self.connect()

    def connect(self):  # 设置槽函数与按钮连接
        self.pushButton_StepRun.clicked.connect(self.Step_Run)
        self.pushButton_Run.clicked.connect(self.Run)
        self.Music_play.clicked.connect(self.music_play)
        self.player.positionChanged.connect(self.Play_State)
        self.Music_play_pause.clicked.connect(self.Play_Pause)
        self.Music_Slider.sliderPressed.connect(self.Play_Pause)
        self.Music_Slider.sliderReleased.connect(self.Play_translate)
        self.pushButton_SaveFile.clicked.connect(self.Save_File)
        self.pushButton_ImportFile.clicked.connect(self.Import_File)

    def vtk_close(self):  # 关闭窗口时同时关闭vtkWidget
        self.vtkWidget.close()

    def comobox_init(self):  # 初始化下拉框，将音乐名称填充
        for dirpath, dirname, file in walk('./resources/music'):
            pass
        self.Music_list.addItems(file)

    def music_play_init(self):  # 初始化音乐播放器
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVolume(100)
        self.Play_flag = 1

    def music_play(self):  # 播放音乐
        try:
            music_file = self.Music_list.currentText()
            if music_file != '':
                self.url = QtCore.QUrl.fromLocalFile('./resources/music/' + music_file)
                self.content = QtMultimedia.QMediaContent(self.url)
                self.player.setMedia(self.content)
                self.player.play()
                self.Play_State()
        except Exception:
            temp = "Error"
        else:
            temp = "OK"
        self.textBrowser.append('>>> ' + 'Play ' + music_file + '  [' + temp + ']')

    def formatTime(self, num):  # 对音乐的长度格式进行规范输出
        num = int(num)
        if num > 0:
            minutes = str(int(num / 60 + 100))[1:3]
            seconds = str(int(num % 60 + 100))[1:3]
            return str(minutes) + ':' + str(seconds)
        return "00:00"

    def Play_State(self):  # 播放过程中自动更新时间显示和进度条
        dur = int(self.player.position() / 1000)
        time = int(self.player.duration() / 1000)
        self.Music_label.setText("%s/%s" % (self.formatTime(dur), self.formatTime(time)))
        if time != 0 and self.Play_flag == 1:
            self.Music_Slider.setValue(int(dur/time*100))

    def Play_translate(self):  # 用进度条控制音乐播放
        # self.player.pause()
        self.Play_flag = (self.Play_flag + 1) % 2
        time = self.player.duration()
        value = self.Music_Slider.value() * time / 100
        self.player.setPosition(int(value))
        self.player.play()

    def Play_Pause(self):  # 切换播放与暂停模式
        if self.Play_flag == 1:
            self.player.pause()
            self.Music_play_pause.setText('播放')
        elif self.Play_flag == 0:
            self.player.play()
            self.Music_play_pause.setText('暂停')
        self.Play_flag = (self.Play_flag + 1) % 2

    def Step_Run(self):
        try:
            eval('tello.' + self.textEdit.toPlainText())
        except Exception:
            temp = "Error"
        else:
            temp = "OK"
        # self.textBrowser.setText(str(temp))
        self.textBrowser.append('>>> ' + 'tello.' + self.textEdit.toPlainText() + '  [' + temp + ']')

    def Run(self):
        try:
            exec(self.textEdit.toPlainText())
        except Exception:
            temp = "Error"
        else:
            temp = "OK"
        self.textBrowser.append('>>> ' + self.textEdit.toPlainText() + '  [' + temp + ']\n')

    # def Pause(self):

    def Save_File(self):
        try:
            strText = self.textEdit.toPlainText()
            [year, mon, mday, hour, minute, sec, wday, yday, isdst] = time.localtime()
            file = open('./log/' + str(year) + str(mon) + str(mday) + str(hour) + str(minute) + '.txt', 'w')
            file.write(strText)
            file.close()
        except Exception as e:
            temp = str(e)
        else:
            temp = 'OK'
        self.textBrowser.append('>>> ' + 'Save File' + '  [' + temp + ']\n')

    def Import_File(self):
        try:
            [file_path, temp] = QFileDialog.getOpenFileName(self, '选择需要导入的文件', './log')
            print(file_path)
            file = open(file_path, 'r')
            strText = file.read()
            self.textEdit.setText(str(strText))
        except Exception as e:
            temp = str(e)
        else:
            temp = 'OK'
        self.textBrowser.append('>>> ' + 'Import File' + '  [' + temp + ']\n')

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, u'警告', u'确认退出?', QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.No)
        # QtWidgets.QMessageBox.question(self,u'弹窗名',u'弹窗内容',选项1,选项2)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()  # 关闭窗口
        else:
            event.ignore()  # 忽视点击X事件

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainPageWindow()
    tello_list = []
    color = ['red', 'gold', 'blue', 'green', 'c']
    for i in range(5):
        temp = Drone(color[i])
        tello_list.append(temp)

    tello = Drone_fly(demo.vtkWidget, tello_list)
    app.aboutToQuit.connect(demo.vtk_close)
    sys.exit(app.exec_())
