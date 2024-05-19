import sys
import psutil
import os
import shutil
import time
import hashlib
from datetime import datetime
from tqdm import tqdm
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from UI import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
import sys


class USB_handler(QThread):
    new_usb_signal = pyqtSignal(str)
    removed_usb_signal = pyqtSignal(str)

    def __init__(self, ui, index):
        super().__init__()
        self.usbs = []
        self.index = index
        self.priority_extensions = [['.docx', '.pdf', '.png', '.jpeg', '.exe'],
                                    ['.txt', '.doc', '.pdf', '.png', '.pptx'],
                                    ['.pptx', '.txt', '.docx', '.pdf', '.png'],
                                    ['.docx', '.pdf', '.png', '.zip', '.rar'],
                                    ['.docx', '.pdf', '.png', '.jpeg', '.exe']]
        self.copied_files = []
        self.ui = ui 
        self.running = True

    @staticmethod
    def list_usb_devices():
        partitions = psutil.disk_partitions()
        usb_devices = [p.device for p in partitions if 'removable' in p.opts]
        return usb_devices

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
                    self.copy_to_tracking(device)

            if removed_devices:
                for device in removed_devices:
                    self.removed_usb_signal.emit(device)

            self.usbs = current_usb_devices
            time.sleep(2)

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
        self.tray_icon.show()  
    
    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.restore_window()
            
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



