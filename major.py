import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QBoxLayout, QHBoxLayout, QVBoxLayout, QCheckBox, QStyle, QAbstractItemView
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt, QUrl, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QAudioInput
#Main
class AudioApplication (QWidget):
    
    path = "x"
    file_name="x"
    number5=0
    
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
        
    #Setting
    def settings(self):
        self.setWindowTitle("Aud-Just")
        self.setGeometry(200,200,1000,650)
    
    
    #Design
    def initUI(self):
        self.title = QLabel("Trans Speed (Slow to Fast)")
        self.order_list=QListWidget()
        self.file_list=QListWidget()
        self.file_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.file_list.setDropIndicatorShown(True)
        self.btn_opener= QPushButton("Choose a file")
        self.btn_play = QPushButton("Play")
        self.btn_pause= QPushButton("Pause")
        self.btn_resume= QPushButton("Resume")
        self.btn_next= QPushButton("Next")
        self.btn_reset= QPushButton("Reset")
        self.box_loop=QCheckBox("Loop")
        self.box_auto_cont=QCheckBox("Auto /n Transition")
        
        #Deactivate for now
        self.btn_pause.setDisabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_next.setDisabled(True)
        self.btn_reset.setDisabled(True)
        self.box_loop.setDisabled(True)
        self.box_auto_cont.setDisabled(True)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(150)
        self.slider.setValue(100)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)
        
        self.sliderT = QSlider(Qt.Orientation.Horizontal)
        self.sliderT.setMinimum(0)
        self.sliderT.setMaximum(10000)
        self.sliderT.setValue(1000)
        self.sliderT.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.sliderT.setTickInterval(1000)
        
        #Write a function to change this number for the speed, though 
        self.slider_text = QLabel("Speed: 100x")
        self.slider_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.sliderT_text = QLabel("Transition: 5")
        self.sliderT_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider_text)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.box_loop)
        slider_layout.addWidget(self.box_auto_cont)
        
        sliderT_layout = QHBoxLayout()
        sliderT_layout.addWidget(self.sliderT_text)
        sliderT_layout.addWidget(self.sliderT)
        
        
        self.master = QVBoxLayout()
        row = QHBoxLayout()
        col0 = QVBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        
        self.master.addWidget(self.title)
        self.master.addLayout(slider_layout)
        self.master.addLayout(sliderT_layout)
        
        col0.addWidget(self.order_list)
        col1.addWidget(self.file_list)
        col2.addWidget(self.btn_opener)
        col2.addWidget(self.btn_play)
        col2.addWidget(self.btn_pause)
        col2.addWidget(self.btn_resume)
        col2.addWidget(self.btn_next)
        col2.addWidget(self.btn_reset)
        
        row.addLayout(col0)
        row.addLayout(col1)
        row.addLayout(col2)
        
        self.master.addLayout(row)
        self.setLayout(self.master)
        
        
        
        #audio classes
        self.audio_output1= QAudioOutput()
        self.audio_output2=QAudioOutput()
        self.media_player1 =QMediaPlayer()
        self.media_player2=QMediaPlayer()
        self.media_player1.setAudioOutput(self.audio_output1)
        self.media_player2.setAudioOutput(self.audio_output2)
        self.media_player=self.media_player1
        self.current_volume=self.audio_output1.volume()
        self.interval=1000

        self.fade_in_anim = QPropertyAnimation(self.audio_output2, b"volume")
        self.fade_in_anim.setDuration(self.interval)
        self.fade_in_anim.setStartValue(0.01)
        self.fade_in_anim.setEndValue(self.audio_output2.volume)
        self.fade_in_anim.setEasingCurve(QEasingCurve.Type.Linear)
        self.fade_in_anim.setKeyValueAt(0.01, 0.01)
        self.fade_in_anim.finished.connect(self.refresh)

        self.fade_out_anim = QPropertyAnimation(self.audio_output1, b"volume")
        self.fade_out_anim.setDuration(self.interval)
        self.fade_out_anim.setStartValue(self.current_volume)
        self.fade_out_anim.setEndValue(0)
        self.fade_out_anim.setEasingCurve(QEasingCurve.Type.Linear)
        self.fade_out_anim.setKeyValueAt(0.01, self.current_volume)
        self.fade_out_anim.finished.connect(self.media_player1.stop)
    #style(needs CSS to work)  
    def style(self):
        self.setStyleSheet("""
                           Qwidget{
                                background-color: #E6C15C;
                           }
                           
                           QPushButton{
                                background-color: #758C32
                                padding:15px;
                                border-radius: 9px;
                                color: #333;
                           }
                           QPushButton:hover{
                                background-color: #172B23;
                                color: #E6C15C;
                           }
                           
                           QLabel{
                               color: #333;
                           }
                           
                           #title{
                               font-family: Papyrus;
                               font-size: 40px;
                           }
                           
                           QListWidget{
                               color: #333;
                           }
                           """)
    #animations 
    
    
    
    #Event Handler
    def event_handler(self):
        self.slider.valueChanged.connect(self.update_slider)
        self.sliderT.valueChanged.connect(self.update_sliderT)
        self.btn_opener.clicked.connect(self.open_file)
        self.btn_play.clicked.connect(self.play_audio)
        self.btn_pause.clicked.connect(self.pause_audio)
        self.btn_next.clicked.connect(self.next_audio)
        self.btn_resume.clicked.connect(self.resume_audio)
        self.btn_reset.clicked.connect(self.reset_audio)
        self.box_loop.stateChanged.connect(self.loop_audio)
        self.media_player.mediaStatusChanged.connect(self.auto_cont_audio)
        
        
    #Change slider speed label 
    def update_slider(self):
        speed = self.slider.value() /100
        self.slider_text.setText(f"Speed:{speed:.2f}x")
        #think about if you want to keep this in
        self.media_player.setPlaybackRate(self.slider.value()/100.0)
        
    def update_sliderT(self):
        tspeed = self.sliderT.value()/1000
        self.sliderT_text.setText(f"Period:{tspeed:.2f}secs")
        #think about if you want to keep this in
        self.interval=(self.sliderT.value())

    #open a folder of files
    def open_file(self):
        global path
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if path:
            self.file_list.clear()
            for file_name in os.listdir(path):
                if file_name.endswith(".mp3") or file_name.endswith(".wav"):
                    self.file_list.addItem(file_name)
                    self.order_list.addItem(str(self.file_list.count()))
            
        else:
            file, _=QFileDialog.getOpenFileName(self,"Select File", filter="Audio Files(*.mp3)" )
            if file:
                self.file_list.clear()
                self.file_list.addItem(os.path.basename(file))
        self.box_loop.setEnabled(True)
        self.box_auto_cont.setEnabled(True)
                
    #playing 
    
    def play_audio(self):
        if self.file_list.selectedItems():
            global file_name
            file_name = self.file_list.selectedItems()[0].text()
            folder_path = path
            file_path = os.path.join(folder_path,file_name)
            file_url = QUrl.fromLocalFile(file_path)
            self.media_player.setSource(file_url)
            self.media_player.setPlaybackRate(self.slider.value()/100.0)
            self.interval=(self.sliderT.value())
            self.current_volume=self.audio_output1.volume()
            self.media_player.play()
            
            self.btn_pause.setEnabled(True)
            self.btn_resume.setDisabled(True)
            self.btn_next.setEnabled(True)
            self.btn_reset.setEnabled(True)
            self.btn_play.setEnabled(True)
            self.box_loop.setEnabled(True)
            self.box_auto_cont.setEnabled(True)
    def pause_audio(self):
        self.media_player.pause()
        self.btn_pause.setDisabled(True)
        self.btn_resume.setEnabled(True)
        self.btn_next.setDisabled(True)
    
    def resume_audio(self):
        self.media_player.play()
        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)
        
    def next_audio(self):
        self.transition()
    
    def transition(self):
        self.fade_out_anim.setStartValue(.5)
        if(self.sliderT.value()!=0):
            self.fade_out_anim.start()
        self.media_player1=self.media_player
        self.media_player=self.media_player2
        number5=self.file_list.currentRow()
        self.file_list.clearSelection()
        if (number5+1)<self.file_list.count():
            self.file_list.setCurrentRow(number5+1)
            self.audio_output2.setVolume(0.01)
            self.fade_in_anim.setEndValue(.5)
            self.play_audio()
            if(self.sliderT.value()!=0):
                self.fade_in_anim.start()
        
    def reset_audio(self):
        if self.media_player.isPlaying():
            self.media_player.stop()
            
        self.media_player.setPosition(0)
        self.media_player.setPlaybackRate(self.slider.value()/100.0)
        self.interval=(self.sliderT.value())
        self.media_player.play()        
        
        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_reset.setEnabled(True)
        self.btn_play.setEnabled(True)
    
    def loop_audio(self):
        if self.box_loop.isChecked():
            self.media_player.setLoops(-1)
        else:
            self.media_player.setLoops(1)
    
    def auto_cont_audio(self):
        if self.media_player.mediaStatus() == self.media_player.MediaStatus.EndOfMedia and self.box_auto_cont.isChecked():
                self.transition()
        
                
    def refresh(self):
        self.media_player.setAudioOutput(self.audio_output2)
                
       
    
    def clear_folder(self):
        self.file_list.clear()
        
        
#BoiledCrab
if __name__ in "__main__":
    app = QApplication([])
    main = AudioApplication()
    main.show()
    app.exec()