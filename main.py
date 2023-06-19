import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableView, QVBoxLayout, \
    QWidget, QFileDialog, QTabWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import polars as pl
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("CSV Viewer")

        self.table = QTableView(self)
        self.button = QPushButton("Load CSV", self)

        # Create Tabs
        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab_widget.addTab(self.tab1, "Loading Data")
        self.tab_widget.addTab(self.tab2, "Metadata")
        self.tab_widget.addTab(self.tab3, "Synthesize Data")

        # Add elements to each tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.button)
        self.tab1.layout.addWidget(self.table)
        self.tab1.setLayout(self.tab1.layout)

        self.metadata_label = QLabel(self.tab2)
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.metadata_label)
        self.tab2.setLayout(self.tab2.layout)

        self.tab3.layout = QVBoxLayout(self)
        self.tab3.setLayout(self.tab3.layout)

        self.setCentralWidget(self.tab_widget)

        self.button.clicked.connect(self.load_csv)

    def load_csv(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "CSV Files (*.csv)",
                                                  options=options)
        if fileName:
            df = pl.read_csv(fileName)  # load csv as polars dataframe
            pandas_df = df.to_pandas()  # convert it to pandas for display in QTableView

            # display dataframe metadata
            metadata = pandas_df.describe(include='all').transpose()
            self.metadata_label.setText(str(metadata))

            model = pandasModel(pandas_df)
            self.table.setModel(model)


class pandasModel(QStandardItemModel):
    def __init__(self, data, parent=None):
        QStandardItemModel.__init__(self, parent)
        self._data = data
        for row in self._data.values:
            data_row = [QStandardItem("{}".format(x)) for x in row]
            self.appendRow(data_row)

        self.setHorizontalHeaderLabels(self._data.columns)


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
