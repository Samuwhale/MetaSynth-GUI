import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QFileDialog, QTextEdit, QSpinBox, QHBoxLayout, QMessageBox)

import polars as pl
import metasynth as ms

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.metadata = None

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.load_dataset_btn = QPushButton('Load Dataset')
        self.load_dataset_btn.clicked.connect(self.load_dataset)
        vbox.addWidget(self.load_dataset_btn)

        self.save_metadata_btn = QPushButton('Save Metadata')
        self.save_metadata_btn.clicked.connect(self.save_metadata)
        vbox.addWidget(self.save_metadata_btn)

        self.load_metadata_btn = QPushButton('Load Metadata')
        self.load_metadata_btn.clicked.connect(self.load_metadata)
        vbox.addWidget(self.load_metadata_btn)

        self.preview_metadata_btn = QPushButton('Preview Metadata')
        self.preview_metadata_btn.clicked.connect(self.preview_metadata)
        vbox.addWidget(self.preview_metadata_btn)

        hbox = QHBoxLayout()
        self.rows_label = QLabel("Rows:")
        hbox.addWidget(self.rows_label)
        self.rows_spinbox = QSpinBox()
        self.rows_spinbox.setRange(1, 10000)
        hbox.addWidget(self.rows_spinbox)
        self.generate_data_btn = QPushButton('Generate Synthetic Data')
        self.generate_data_btn.clicked.connect(self.generate_data)
        hbox.addWidget(self.generate_data_btn)
        vbox.addLayout(hbox)

        self.save_data_btn = QPushButton('Save Synthetic Data')
        self.save_data_btn.clicked.connect(self.save_data)
        vbox.addWidget(self.save_data_btn)

        self.log_label = QLabel("Logs:")
        vbox.addWidget(self.log_label)
        self.log = QTextEdit()
        vbox.addWidget(self.log)

        self.setLayout(vbox)
        self.setWindowTitle('MetaSynth GUI')

    def preview_metadata(self):
        if self.metadata:
            # Convert metadata to JSON
            metadata_json = self.metadata.to_json("metadatatest.json")

            # Show JSON in a message box
            msg = QMessageBox()
            msg.setWindowTitle("Metadata Preview")
            msg.setText(str(metadata_json))
            msg.exec_()
        else:
            self.log.append("No metadata available. Please load a dataset first.")

    def load_dataset(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')

        if fname[0]:
            self.log.append(f"Loading dataset from {fname[0]}")
            df = pl.read_csv(fname[0])
            self.metadata = ms.MetaDataset.from_dataframe(df)
            self.log.append(f"Successfully created metadata from {fname[0]}")

    def save_metadata(self):
        if self.metadata:
            fname = QFileDialog.getSaveFileName(self, 'Save file', './')
            if fname[0]:
                self.metadata.to_json(fname[0])
                self.log.append(f"Metadata saved to {fname[0]}")
        else:
            self.log.append("No metadata available. Please load a dataset first.")

    def load_metadata(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')

        if fname[0]:
            self.log.append(f"Loading metadata from {fname[0]}")
            self.metadata = ms.MetaDataset.from_json(fname[0])
            self.log.append(f"Successfully loaded metadata from {fname[0]}")

    def generate_data(self):
        if self.metadata:
            self.synthetic_data = self.metadata.synthesize(self.rows_spinbox.value())
            self.log.append(f"Generated {self.rows_spinbox.value()} rows of synthetic data.")
        else:
            self.log.append("No metadata available. Please load a dataset or metadata first.")

    def save_data(self):
        if hasattr(self, 'synthetic_data'):
            fname = QFileDialog.getSaveFileName(self, 'Save file', './')
            if fname[0]:
                self.synthetic_data.write_csv(fname[0])
                self.log.append(f"Synthetic data saved to {fname[0]}")
        else:
            self.log.append("No synthetic data available. Please generate data first.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
