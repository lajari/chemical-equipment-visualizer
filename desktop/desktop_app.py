import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QFileDialog, QTextEdit, QLabel
)
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000/api/upload/"

class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FOSSEE CSV Analyzer (Desktop)")
        self.setGeometry(200, 200, 500, 500)

        self.label = QLabel("No file selected")
        self.label.setFont(QFont("Arial", 10))

        self.choose_btn = QPushButton("Choose CSV File")
        self.upload_btn = QPushButton("Upload & Analyze")

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.choose_btn)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.output)

        self.setLayout(layout)

        self.file_path = None
        self.choose_btn.clicked.connect(self.choose_file)
        self.upload_btn.clicked.connect(self.upload_file)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.file_path = file_path
            self.label.setText(file_path)

    def upload_file(self):
        if not self.file_path:
            self.output.setText("Please choose a CSV file first.")
            return

        try:
            with open(self.file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(API_URL, files=files)

            if response.status_code == 200:
                data = response.json()
                self.display_result(data)
                self.plot_chart(data["type_distribution"])
            else:
                self.output.setText("Upload failed. Status code: " + str(response.status_code))
        except Exception as e:
            self.output.setText("Error: " + str(e))

    def display_result(self, data):
        text = f"""
Total Count: {data['total_count']}
Average Flowrate: {data['avg_flowrate']}
Average Pressure: {data['avg_pressure']}
Average Temperature: {data['avg_temperature']}
Type Distribution: {data['type_distribution']}
"""
        self.output.setText(text)

    def plot_chart(self, type_dist):
        names = list(type_dist.keys())
        values = list(type_dist.values())

        plt.figure()
        plt.bar(names, values)
        plt.title("Equipment Type Distribution")
        plt.xlabel("Equipment Type")
        plt.ylabel("Count")
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
