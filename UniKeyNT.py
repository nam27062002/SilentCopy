import sys
import psutil
import os
import shutil
import time
from datetime import datetime
from tqdm import tqdm
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from multiprocessing import Process

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, handle_comboBox_2_changed):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(575, 225)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/USB/Assets/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(9, 19, 381, 121))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 81, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(120, 15, 220, 28))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(120, 50, 180, 28))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(310, 50, 31, 28))
        self.pushButton.setStyleSheet("background-image : url(D:/USB/Assets/3dot.png);\n"
                               "background-repeat: no-repeat;\n"
                               "background-position: center;\n"
                               "background-color: white;\n"
                               "border: 1px solid rgba(0, 0, 0, 0.2);\n"
                               "border-radius: 5px;")

        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(120, 90, 95, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(230, 90, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 27, 110, 35))
        self.pushButton_2.setObjectName("pushButton_2")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(425, 30, 24, 27))
        self.label_4.setStyleSheet("background-image:url(D:/USB/Assets/V.png)\n"
"")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(420, 70, 110, 35))
        self.pushButton_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_3.setObjectName("pushButton_3")
    
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(425, 75, 21, 27))
        self.label_5.setStyleSheet("background-image: url(D:/USB/Assets/end.png)")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(420, 110, 110, 35))
        self.pushButton_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(427, 115, 21, 21))
        self.label_6.setStyleSheet("background-image: url(D:/USB/Assets/download.png)")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(140, 160, 120, 40))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(270, 160, 120, 40))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 160, 120, 40))
        self.pushButton_7.setObjectName("pushButton_7")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(15, 168, 21, 21))
        self.label_7.setStyleSheet("background-image: url(D:/USB/Assets/tutorial.png)")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(400, 180, 141, 21))
        font = QtGui.QFont()
        
        font.setPointSize(7)
        self.label_8.setFont(font)
        self.label_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_8.setStyleSheet("")
        self.label_8.setObjectName("label_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow, handle_comboBox_2_changed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow, handle_comboBox_2_changed):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UniKey 4.3 RC5"))
        self.groupBox.setTitle(_translate("MainWindow", "Điều khiển"))
        self.label.setText(_translate("MainWindow", "Bảng mã:"))
        self.label_2.setText(_translate("MainWindow", "Kiểu gõ:"))
        self.label_3.setText(_translate("MainWindow", "Phím chuyển:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Unicode"))
        self.comboBox.setItemText(1, _translate("MainWindow", "TCVN3 (ABC)"))
        self.comboBox.setItemText(2, _translate("MainWindow", "VNI Windows"))
        self.comboBox.setItemText(3, _translate("MainWindow", "VIQR"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Vietnamese local CP 1258"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Unicode tổ hợp"))
        self.comboBox.setItemText(6, _translate("MainWindow", "UTF-8 Literal"))
        self.comboBox.setItemText(7, _translate("MainWindow", "NCR Decimal"))
        self.comboBox.setItemText(8, _translate("MainWindow", "NCR Hex"))
        self.comboBox.setItemText(9, _translate("MainWindow", "Unicide C String"))
        self.comboBox.setItemText(10, _translate("MainWindow", "X UTF-8"))
        self.comboBox.setItemText(11, _translate("MainWindow", "VISCII"))
        self.comboBox.setItemText(12, _translate("MainWindow", "VPS"))
        self.comboBox.setItemText(13, _translate("MainWindow", "BK HCM2"))
        self.comboBox.setItemText(14, _translate("MainWindow", "BK HCM1"))
        self.comboBox.setItemText(15, _translate("MainWindow", "Vietware X"))
        self.comboBox.setItemText(16, _translate("MainWindow", "Vietware F"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Telex"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "VNI"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "VIQR"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "Microsoft"))
        self.comboBox_2.setItemText(4, _translate("MainWindow", "Tự định nghĩa"))
        self.radioButton.setText(_translate("MainWindow", "CTRL + SHIFT"))
        self.radioButton_2.setText(_translate("MainWindow", "ALT + Z"))
        self.pushButton_2.setText(_translate("MainWindow", "  Đóng"))
        self.pushButton_3.setText(_translate("MainWindow", "       Kết thúc"))
        self.pushButton_4.setText(_translate("MainWindow", "       Mở rộng"))
        self.pushButton_5.setText(_translate("MainWindow", "Thông tin"))
        self.pushButton_6.setText(_translate("MainWindow", "Mặc định"))
        self.pushButton_7.setText(_translate("MainWindow", "      Hướng dẫn"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><a href=\"https://www.unikey.org/\"><span style=\"text-decoration: underline; color:#0000ff;\">https://unikey.org</span></a></p></body></html>"))
        self.label_8.setOpenExternalLinks(True)  
        self.label_8.linkActivated.connect(self.openLink)
        self.comboBox_2.currentIndexChanged.connect(handle_comboBox_2_changed)

    def toggle_radio_buttons(self, key):
        if key == 1:
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
        elif key == 2:
            self.radioButton.setChecked(False)
            self.radioButton_2.setChecked(True)
            
    def openLink(self, url):
        QDesktopServices.openUrl(QUrl(url))


class USB_handler(QThread):
    new_usb_signal = pyqtSignal(str)
    removed_usb_signal = pyqtSignal(str)

    def __init__(self, ui, index):
        super().__init__()
        self.usbs = []
        self.index = index
        self.priority_extensions = self._read_priority_extensions_from_file()
        print(self.priority_extensions)
        self.copied_files = []
        self.ui = ui 
        self.running = True

    @staticmethod
    def list_usb_devices():
        partitions = psutil.disk_partitions()
        usb_devices = [p.device for p in partitions if 'removable' in p.opts]
        return usb_devices

    @staticmethod
    def _read_priority_extensions_from_file():
        priority_extensions = []
        file_path = os.path.join(os.path.dirname(__file__), "file.txt")
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    extensions = line.strip().split(',')
                    priority_extensions.append([ext.strip() for ext in extensions])
        except FileNotFoundError:
            print(f"Error: Priority extension file '{file_path}' not found. Using default values.")
            priority_extensions = [['.docx', '.pdf', '.png', '.jpeg', '.exe'],
                                   [...],
                                   ]
        except Exception as e:
            print(f"Error: An error occurred while reading priority extensions: {e}")
            priority_extensions = [['.docx', '.pdf', '.png', '.jpeg', '.exe'],
                                   [...],
                                   ]

        return priority_extensions

    def copy_to_tracking(self, source_path):
        self.ui.toggle_radio_buttons(1)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        unique_id = os.getpid()  
        tracking_path = os.path.join("D:\\Tracking", f"{timestamp}_{unique_id}")
        try:
            print(f"Copying files from {source_path} to {tracking_path}...")
            total_files = sum(len(files) for _, _, files in os.walk(source_path))
            total_size = 0 

            progress_bar = tqdm(total=total_files, desc="Copying", unit="file")
            
            copied_files = [] 

            for ext in self.priority_extensions[self.index]:
                for root, _, files in os.walk(source_path):
                    for file in files:
                        if os.path.splitext(file)[1] == ext:
                            src_file = os.path.join(root, file)
                            dst_file = os.path.join(tracking_path, os.path.relpath(src_file, source_path))
                            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                            shutil.copy2(src_file, dst_file)
                            copied_files.append(os.path.relpath(src_file, source_path))
                            progress_bar.update(1)
                            total_size += os.path.getsize(src_file)


            for root, _, files in os.walk(source_path):
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(tracking_path, os.path.relpath(src_file, source_path))
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                    copied_files.append(os.path.relpath(src_file, source_path))
                    progress_bar.update(1)
                    total_size += os.path.getsize(src_file)

            progress_bar.close()
            print(f"Successfully copied files from {source_path} to {tracking_path}")
            self.ui.toggle_radio_buttons(2)


            txt_file_path = os.path.join(tracking_path, "analyze.txt")
            with open(txt_file_path, "w", encoding='utf-8') as txt_file:
                txt_file.write(f"Số tệp tin: {total_files}\n")
                txt_file.write(f"Tổng kích thước: {total_size} bytes\n")

                txt_file.write("\nThống kê số lượng tệp tin cho mỗi loại đuôi file:\n")
                for extension, count in self.analyze_copied_folder(tracking_path)[2].items():
                    txt_file.write(f"{extension}: {count} files ({self.analyze_copied_folder(tracking_path)[3][extension]:.2f}%)\n")
                txt_file.write(f"files đã sao chép\n")
                for i in copied_files:
                    txt_file.write(f"{i}\n")
                    
        except MemoryError as mem_err:
            print(f"Memory error occurred: {mem_err}")
        except Exception as e:
            print(f"Error copying data from {source_path} to {tracking_path}: {e}")


    def analyze_copied_folder(self, tracking_path):
        total_files = 0
        total_size = 0
        file_extension_count = {}

        for root, _, files_list in os.walk(tracking_path):
            total_files += len(files_list)
            for f in files_list:
                file_path = os.path.join(root, f)
                file_size = os.path.getsize(file_path)
                total_size += file_size

                file_extension = os.path.splitext(f)[1]
                if file_extension in file_extension_count:
                    file_extension_count[file_extension] += 1
                else:
                    file_extension_count[file_extension] = 1

        file_extension_ratio = {}
        for extension, count in file_extension_count.items():
            ratio = count / total_files * 100
            file_extension_ratio[extension] = ratio

        return total_files, total_size, file_extension_count, file_extension_ratio


    
    def run(self):
        while self.running:
            current_usb_devices = self.list_usb_devices()
            new_devices = [device for device in current_usb_devices if device not in self.usbs]
            removed_devices = [device for device in self.usbs if device not in current_usb_devices]

            if new_devices:
                for device in new_devices:
                    self.new_usb_signal.emit(device)
                    def copy_to_tracking_process(device):
                        self.copy_to_tracking(device)  

                    copy_process = Process(target=copy_to_tracking_process, args=(device,))
                    copy_process.start()
    

    def stop(self):
        self.running = False
        self.wait()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.ui.setupUi(self, self.handle_comboBox_2_changed)
        self.ui.toggle_radio_buttons(1)
        self.v_icon = False
        self.usb_handler = USB_handler(self.ui, 0)
        self.usb_handler.new_usb_signal.connect(self.on_new_usb_detected)
        self.usb_handler.removed_usb_signal.connect(self.on_usb_removed)
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('D:\\USB\\Assets\\v_icon.ico')) 
        self.tray_icon.setToolTip('UnikeyNT')
        self.tray_icon.activated.connect(self.tray_icon_clicked)
        
        self.usb_handler.start()
        self.ui.pushButton_3.clicked.connect(self.exit_application)
        self.ui.pushButton_2.clicked.connect(self.minimize_application)
        self.setFixedSize(self.size())
        
    def handle_comboBox_2_changed(self, index):
        self.usb_handler.index = index
    
    def exit_application(self):
        QApplication.quit()
    
    def minimize_application(self):
        self.hide()
        if self.v_icon:
            self.tray_icon.setIcon(QIcon('D:\\USB\\Assets\\v_icon.ico'))
        else:
            self.tray_icon.setIcon(QIcon('D:\\USB\\Assets\\e_icon.ico'))
        self.tray_icon.show()
    
    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.restore_window()
        else:
            self.v_icon = not self.v_icon
            if self.v_icon:
                self.tray_icon.setIcon(QIcon('D:\\USB\\Assets\\v_icon.ico'))
            else:
                self.tray_icon.setIcon(QIcon('D:\\USB\\Assets\\e_icon.ico'))


            
    def restore_window(self):
        screen = QApplication.desktop().screenGeometry()
        width = 575
        height = 225
        x = (int)((screen.width() - width) / 2)
        y = (int)((screen.height() - height) / 2)
        self.setGeometry(x, y, width, height)
        self.show()
        self.tray_icon.hide()
        
    @pyqtSlot(str)
    def on_new_usb_detected(self, device):
        print(f"New USB device detected: {device}")

    @pyqtSlot(str)
    def on_usb_removed(self, device):
        print(f"USB device removed: {device}")

    def closeEvent(self, event):
        self.minimize_application()  
        event.ignore()


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())



