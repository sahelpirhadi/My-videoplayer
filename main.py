from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QHBoxLayout,QVBoxLayout,\
    QStyle, QSlider,QFileDialog
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent                           
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt,QUrl,pyqtSignal
import sys 
class window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("play.ico"))
        self.setWindowTitle("Pyplayer")
        self.setGeometry(400,100,700,500) 
        p = self.palette()
        p.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.darkBlue)
        self.setPalette(p)
        self.create_Player()
    def create_Player(self):
        self.mediaPlayer=QMediaPlayer(None,QMediaPlayer.Flag.VideoSurface)
        videowidget=QVideoWidget()
        self.openBtn=QPushButton('Open Video')
        self.openBtn.clicked.connect(self.open_file)
        self.PlayBtn=QPushButton()
        self.PlayBtn.setEnabled(False)
        self.PlayBtn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.PlayBtn.clicked.connect(self.play_video)
        self.slider=QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
        hbox=QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.PlayBtn)
        hbox.addWidget(self.slider)
        vbox=QVBoxLayout()
        vbox.addWidget(videowidget)
        vbox.addLayout(hbox)
        self.mediaPlayer.setVideoOutput(videowidget)
        self.setLayout(vbox)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
    def open_file(self):
        filename, _ =QFileDialog.getOpenFileName(self)
        if filename !='':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.PlayBtn.setEnabled(True)
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.MediaStatus(1):
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    def mediastate_changed(self):
        if self.mediaPlayer.state()== QMediaPlayer.MediaStatus(1):
           self.PlayBtn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)) 
        else:
            self.PlayBtn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))  
    def position_changed(self,position):
        self.slider.setValue(position)
    def duration_changed(self,duration):
        self.slider.setRange(0,duration)
    def set_position(self,position):
        self.mediaPlayer.setPosition(position)
app=QApplication(sys.argv)
window=window()
window.show()
sys.exit(app.exec_())
