import json
import csv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
    QComboBox, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import pandas as pd  # Cần cài đặt thư viện pandas cho Excel/CSV

class HostManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.json_file = None
        self.data = {"hosts": [], "groups": {}}
        self.init_ui()

    def load_data(self, json_file):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "File không tồn tại!")
            self.data = {"hosts": [], "groups": {}}
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Lỗi", "File JSON không hợp lệ!")
            self.data = {"hosts": [], "groups": {}}

    def save_data(self):
        if not self.json_file:
            QMessageBox.critical(self, "Lỗi", "Chưa chọn file để lưu!")
            return
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def init_ui(self):
        self.setWindowTitle("Quản Lý Hosts - Phạm Thanh Thiệu - 0988.927.177")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()

        # Header
        header = QLabel("Quản Lý Hosts", self)
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        # File Controls
        file_layout = QHBoxLayout()
        load_file_button = QPushButton("Chọn File Hosts")
        load_file_button.clicked.connect(self.select_file)
        file_layout.addWidget(load_file_button)
        main_layout.addLayout(file_layout)

        # Filter & Controls
        filter_layout = QHBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Tất cả")
        self.filter_combo.currentTextChanged.connect(self.filter_hosts)

        add_button = QPushButton("Thêm Host")
        add_button.clicked.connect(self.add_host)

        delete_button = QPushButton("Xóa Host")
        delete_button.clicked.connect(self.delete_selected_hosts)

        import_button = QPushButton("Import")
        import_button.clicked.connect(self.import_data)

        filter_layout.addWidget(QLabel("Lọc theo nhóm:"))
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(add_button)
        filter_layout.addWidget(delete_button)
        filter_layout.addWidget(import_button)
        main_layout.addLayout(filter_layout)

        # Hosts Table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Tên", "IP", "Nhóm", "Mô tả"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_host)
        main_layout.addWidget(self.table)

        main_widget.setLayout(main_layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file hosts", "./config", "JSON Files (*.json)")
        if file_path:
            self.json_file = file_path
            self.load_data(file_path)
            self.filter_combo.clear()
            self.filter_combo.addItem("Tất cả")
            self.filter_combo.addItems(self.data.get("groups", {}).keys())
            self.load_hosts()

    def load_hosts(self):
        self.table.setRowCount(0)
        for host in self.data["hosts"]:
            self.add_table_row(host)

    def add_table_row(self, host):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(host["name"]))
        self.table.setItem(row, 1, QTableWidgetItem(host["ip"]))
        self.table.setItem(row, 2, QTableWidgetItem(host["type"]))
        self.table.setItem(row, 3, QTableWidgetItem(host["description"]))

    def filter_hosts(self):
        group = self.filter_combo.currentText()
        self.table.setRowCount(0)
        for host in self.data["hosts"]:
            if group == "Tất cả" or host["type"] == group:
                self.add_table_row(host)

    def add_host(self):
        self.host_form()

    def edit_host(self):
        row = self.table.currentRow()
        if row == -1:
            return
        name = self.table.item(row, 0).text()
        for host in self.data["hosts"]:
            if host["name"] == name:
                self.host_form(host)
                break

    def host_form(self, host=None):
        dialog = QWidget()
        dialog.setWindowTitle("Thêm/Sửa Host")
        dialog.setGeometry(200, 200, 400, 300)
        layout = QVBoxLayout()

        # Input fields
        name_input = QLineEdit(host["name"] if host else "")
        ip_input = QLineEdit(host["ip"] if host else "")
        type_combo = QComboBox()
        type_combo.addItems(self.data["groups"].keys())
        if host:
            type_combo.setCurrentText(host["type"])
        desc_input = QLineEdit(host["description"] if host else "")

        layout.addWidget(QLabel("Tên:"))
        layout.addWidget(name_input)
        layout.addWidget(QLabel("IP:"))
        layout.addWidget(ip_input)
        layout.addWidget(QLabel("Nhóm:"))
        layout.addWidget(type_combo)
        layout.addWidget(QLabel("Mô tả:"))
        layout.addWidget(desc_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Lưu")
        save_button.clicked.connect(lambda: self.save_host(dialog, host, name_input, ip_input, type_combo, desc_input))
        cancel_button = QPushButton("Hủy")
        cancel_button.clicked.connect(dialog.close)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.show()

    def save_host(self, dialog, host, name_input, ip_input, type_combo, desc_input):
        new_ip = ip_input.text()
        if not host:  # Trường hợp thêm mới
            for existing_host in self.data["hosts"]:
                if existing_host["ip"] == new_ip:
                    QMessageBox.warning(self, "Cảnh báo", f"IP '{new_ip}' đã tồn tại! Vui lòng sửa hoặc sử dụng IP khác.")
                    return
        else:  # Trường hợp sửa
            for existing_host in self.data["hosts"]:
                if existing_host["ip"] == new_ip and existing_host != host:
                    QMessageBox.warning(self, "Cảnh báo", f"IP '{new_ip}' đã tồn tại! Vui lòng sửa hoặc sử dụng IP khác.")
                    return

        new_host = {
            "name": name_input.text(),
            "ip": new_ip,
            "type": type_combo.currentText(),
            "description": desc_input.text()
        }
        if host:
            self.data["hosts"].remove(host)
        self.data["hosts"].append(new_host)
        self.save_data()
        self.load_hosts()
        dialog.close()

    def delete_selected_hosts(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn ít nhất một host để xóa!")
            return

        confirm = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn xóa các host đã chọn?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        rows_to_delete = [row.row() for row in selected_rows]
        for row in sorted(rows_to_delete, reverse=True):
            host_name = self.table.item(row, 0).text()
            self.data["hosts"] = [host for host in self.data["hosts"] if host["name"] != host_name]
            self.table.removeRow(row)

        self.save_data()
        self.load_hosts()

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file để import", "", "Files (*.json *.csv *.xlsx)")
        if not file_path:
            return

        try:
            imported_data = []
            if file_path.endswith(".json"):
                with open(file_path, "r", encoding="utf-8") as f:
                    imported_data = json.load(f)
            elif file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
                imported_data = df.to_dict(orient="records")
            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
                imported_data = df.to_dict(orient="records")
            else:
                raise ValueError("Định dạng file không được hỗ trợ!")

            duplicate_ips = []
            added_hosts = 0

            for host in imported_data:
                if all(key in host for key in ["name", "ip", "type", "description"]):
                    if any(existing_host["ip"] == host["ip"] for existing_host in self.data["hosts"]):
                        duplicate_ips.append(host["ip"])
                    else:
                        self.data["hosts"].append(host)
                        added_hosts += 1
                else:
                    QMessageBox.warning(self, "Cảnh báo", f"Host thiếu thông tin: {host}")

            # Lưu và tải lại dữ liệu
            self.save_data()
            self.load_hosts()

            # Thông báo kết quả
            if duplicate_ips:
                QMessageBox.warning(
                    self,
                    "Cảnh báo",
                    f"Các IP trùng đã bị bỏ qua: {', '.join(duplicate_ips)}"
                )
            QMessageBox.information(
                self,
                "Thành công",
                f"Đã thêm {added_hosts} hosts mới. {len(duplicate_ips)} IP trùng đã bị bỏ qua."
            )

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể import file: {str(e)}")


if __name__ == "__main__":
    app = QApplication([])
    window = HostManagerApp()
    window.show()
    app.exec()
