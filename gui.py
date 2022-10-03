from re import S
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from styles import styles
from PyQt5.QtCore import Qt
import sys
import os
import dotenv

# Initializing translator and keyword searching system.


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.init()

    def init(self):
        self.main_layout = QHBoxLayout()
        self.layout_vertical_for_inputs = QVBoxLayout()

        self.init_image_submitted = False
        self.mask_image_submitted = False

        self.output_image = QLabel(self)
        self.output_image.setStyleSheet(styles.text_style)
        self.output_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Preparing...", self)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop
        )
        self.label.setStyleSheet(styles.text_style)
        self.label.setVisible(False)

        self.environment = os.environ["HOMEPATH"]
        self.dir = os.getcwd()

        self.textInput = QTextEdit()
        self.textInput.setStyleSheet(styles.text_edit_style)
        self.textInput.setPlaceholderText("Enter prompt here")

        self.stepsInput = QSpinBox()
        self.stepsInput.setStyleSheet(styles.spinbox_style)
        self.stepsInput.setRange(1,200)
        self.stepsInput.setValue(25)
        self.stepsInput.setToolTip("Number of Iterations, higher steps higher accuracy and time.")

        self.widthInput = QSpinBox()
        self.widthInput.setStyleSheet(styles.spinbox_style)
        self.widthInput.setRange(1,1920)
        self.widthInput.setValue(512)
        self.widthInput.setToolTip("Width of the output.")

        self.heightInput = QSpinBox()
        self.heightInput.setStyleSheet(styles.spinbox_style)
        self.heightInput.setRange(1,1920)
        self.heightInput.setValue(512)
        self.heightInput.setToolTip("Height of the output.")

        self.init_image_button = QPushButton("Reference Image")
        self.init_image_button.setStyleSheet(styles.inputs_button_style)
        self.init_image_button.clicked.connect(self.init_image_submit)

        self.mask_image_button = QPushButton("Mask Image")
        self.mask_image_button.setStyleSheet(styles.inputs_button_style)
        self.mask_image_button.clicked.connect(self.mask_image_submit)

        self.output_path_button = QPushButton("Output Path")
        self.output_path_button.setStyleSheet(styles.button_style)
        self.output_path_button.clicked.connect(self.modify_output_path)

        self.create_button = QPushButton("Save")
        self.create_button.setStyleSheet(styles.button_style)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet(styles.button_style)
        self.reset_button.clicked.connect(self.reset)

        self.placement()
        self.setLayout(self.main_layout)

    def init_image_submit(self):
        if not self.init_image_submitted:
            self.init_image_path = QFileDialog.getOpenFileName(self, "Reference Image", self.dir)[0]
            self.init_image_button.setText("Selected.")
            if(self.init_image_path != ""):
                self.init_image_submitted = True
        else:
            self.init_image_submitted = False
            self.init_image_path = ""
            self.init_image_button.setText("Reference Image")
            
        

    def mask_image_submit(self):
        if not self.mask_image_submitted:
            self.mask_image_path = QFileDialog.getOpenFileName(self, "Reference Image", self.dir)[0]
            self.mask_image_button.setText("Selected.")
            if(self.mask_image_path != ""):
                self.mask_image_submitted = True
        else:
            self.mask_image_submitted = False
            self.mask_image_path = ""
            self.mask_image_button.setText("Reference Image")

    def reset(self):
        # This function sets all fields to default.
        self.textInput.setText("")
        self.output_image.setPixmap(QtGui.QPixmap(""))
        self.stepsInput.setValue(25)
        self.widthInput.setValue(512)
        self.heightInput.setValue(512)
        self.label.setVisible(False)
        self.init_image_submitted = False
        self.init_image_path = ""
        self.init_image_button.setText("Referance Image")
        self.mask_image_submitted = False
        self.mask_image_path = ""
        self.mask_image_button.setText("Mask Image")

    def placement(self):
        # Layout and widget management.
        buttons_box = QHBoxLayout()
        buttons_box.addWidget(self.output_path_button)
        buttons_box.addWidget(self.create_button)
        buttons_box.addWidget(self.reset_button)

        inputs_box = QHBoxLayout()
        inputs_box.addWidget(self.stepsInput)
        inputs_box.addWidget(self.widthInput)
        inputs_box.addWidget(self.heightInput)
        inputs_box.addWidget(self.init_image_button)
        inputs_box.addWidget(self.mask_image_button)

        outputs_box = QHBoxLayout()
        outputs_box.addWidget(self.label)
        outputs_box.addWidget(self.output_image)

        self.layout_vertical_for_inputs.addWidget(self.textInput)
        self.layout_vertical_for_inputs.addLayout(inputs_box)
        self.layout_vertical_for_inputs.addLayout(buttons_box)
        self.layout_vertical_for_inputs.addLayout(outputs_box)
        self.layout_vertical_for_inputs.addStretch()

        self.main_layout.addStretch()
        self.main_layout.addLayout(self.layout_vertical_for_inputs)
        self.main_layout.addStretch()

    def message_box(self, icon, buttons, title, text):
        # Just a function to simply create message dialogs.
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setStandardButtons(buttons)
        msg.setWindowTitle(title)
        return msg.exec()

    def modify_output_path(self):
        # Modifying output path if needed. The output image will appear in that path.
        self.temp_path = self.dir
        self.dir = QFileDialog.getExistingDirectory(
            None, "Select project folder:", self.environment, QFileDialog.ShowDirsOnly
        )
        if self.dir == "":
            self.dir = self.temp_path

    def error_check(self):


    def generate(self):
        


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setStyleSheet("background-color: rgba(255, 255, 255, .1);")
        self.setGeometry(400, 200, 1200, 600)
        self.startMainMenu()

    def startMainMenu(self):
        self.window = Window(self)
        self.setWindowTitle("Cosmic Mind")
        self.setCentralWidget(self.window)
        self.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())
