import sys
import psutil
import os
import shutil
from datetime import datetime
from tqdm import tqdm
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, pyqtSlot
from UI import Ui_MainWindow

log_file_path = os.path.join(os.path.dirname(__file__), "application.log")
sys.stdout = open(log_file_path, 'w')
sys.stderr = open(log_file_path, 'w')

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
            priority_extensions = [['.docx', '.pdf', '.png', '.jpeg', '.exe']]
        except Exception as e:
            print(f"Error: An error occurred while reading priority extensions: {e}")
            priority_extensions = [['.docx', '.pdf', '.png', '.jpeg', '.exe']]

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

    def check_for_new_devices(self):
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

    def allow_copy(self):
        for device in self.usbs:
            self.new_usb_signal.emit(device)
            self.copy_to_tracking(device)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.ui.setupUi(self, self.handle_comboBox_2_changed)
        self.ui.toggle_radio_buttons(2)
        self.v_icon = False
        self.usb_handler = USB_handler(self.ui, 0)
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('D:\\USB\\Assets\\v_icon.ico')) 
        self.tray_icon.setToolTip('UnikeyNT')
        self.tray_icon.activated.connect(self.tray_icon_clicked)

        self.check_usb_timer = QTimer(self)
        self.check_usb_timer.timeout.connect(self.check_usb_devices_conditionally)
        self.check_usb_timer.start(1000)


        self.usb_handler.new_usb_signal.connect(self.on_new_usb_detected)
        self.usb_handler.removed_usb_signal.connect(self.on_usb_removed)

        self.ui.pushButton_3.clicked.connect(self.exit_application)
        self.ui.pushButton_2.clicked.connect(self.minimize_application)
        self.setFixedSize(self.size())
        self.showUI = True
        
        
    def handle_comboBox_2_changed(self, index):
        self.usb_handler.index = index
    
    def exit_application(self):
        QApplication.quit()
    
    def minimize_application(self):
        self.hide()
        self.showUI = False
        self.set_tray_icon()
        self.tray_icon.show()
    
    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.restore_window()
        else:
            self.v_icon = not self.v_icon
            self.set_tray_icon()

    def set_tray_icon(self):
        if self.v_icon:
            self.tray_icon.setIcon(QIcon('D:\\USB\\Assets\\v_icon.ico'))
            self.usb_handler.allow_copy()
        else:
            self.tray_icon.setIcon(QIcon('D:\\USB\\Assets\\e_icon.ico'))
    
    def restore_window(self):
        self.showUI = True
        screen = QApplication.desktop().screenGeometry()
        width = 575
        height = 225
        x = (int)((screen.width() - width) / 2)
        y = (int)((screen.height() - height) / 2)
        self.setGeometry(x, y, width, height)
        self.show()
        self.tray_icon.hide()

    def closeEvent(self, event):
        self.minimize_application()  
        event.ignore()

    @pyqtSlot(str)
    def on_new_usb_detected(self, device):
        self.v_icon = True
        self.set_tray_icon()

    @pyqtSlot(str)
    def on_usb_removed(self, device):       
        self.v_icon = False
        self.set_tray_icon()
        
    def check_usb_devices_conditionally(self):
        if self.showUI or self.v_icon:
            self.usb_handler.check_for_new_devices()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
