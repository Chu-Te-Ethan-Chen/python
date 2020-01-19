import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import pandas as pd
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy import interpolate

class HW04Window(QMainWindow):
    colorList = ['red', 'orange', 'yellow', 'green', 'blue', 'black', 'pink', 'olive']
    symbolList = ['o', 's', 'D', '^']
    lineList = ['-',':','--','-.']
    weightList = ['normal', 'bold', 'heavy']
    fontList = ['Arial Unicode MS', 'Times New Roman', 'Courier New']
    tagList = ['True', 'Flase']
    data = pd.DataFrame()
    def __init__(self):
        super().__init__()
        loadUi("lint_chart_GUI.ui", self)
        self.labelExcelFilename.setText("Select Excel File from Menu")
        self.actionMenuFile.triggered.connect(self.actionMenuFile_triggered)
        self.lineEditX.setText('12')
        self.lineEditY.setText('10')
        self.comboFont.addItems(self.fontList)
        self.comboFont.setCurrentIndex(0)
        self.lineEditFontSize.setText('20')
        self.comboWeight.addItems(self.weightList)
        self.comboWeight.setCurrentIndex(0)
        self.lineEditAxisLineWidth.setText('2')
        self.lineEditAxisTitleSize.setText('24')
        self.lineEditAxisLabelSize.setText('24')
        self.comboTag.addItems(self.tagList)
        self.comboTag.setCurrentIndex(0)
        self.comboMarkerType.addItems(self.symbolList)
        self.comboMarkerType.setCurrentIndex(0)
        self.comboMarkerColor.addItems(self.colorList)
        self.comboMarkerColor.setCurrentIndex(0)
        self.lineEditMarkerSize.setText('10')
        self.comboLineStyle.addItems(self.lineList)
        self.comboLineStyle.setCurrentIndex(0)
        self.comboLineColor.addItems(self.colorList)
        self.comboLineColor.setCurrentIndex(0)
        self.lineEditLineWidth.setText('2')
        self.buttonPlot.clicked.connect(self.buttonPlot_clicked)
        self.actionMenuExit.triggered.connect(self.actionMenuExit_triggered)
        self.buttonAddSeries.clicked.connect(self.buttonAddSeries_clicked)
        self.buttonDeleteSeries.clicked.connect(self.buttonDeleteSeries_clicked)
        self.show()
    def actionMenuFile_triggered(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx);;All Files (*)")
        if filename:
            self.labelExcelFilename.setText(filename)
            df = pd.read_excel(self.labelExcelFilename.text(), index_col=0)
            self.data = self.data.append(df)
            self.comboX.clearEditText()
            self.comboY.clearEditText()
            self.comboX.addItems(df.columns.values.tolist())
            self.comboY.addItems(df.columns.values.tolist())
    def actionMenuExit_triggered(self):
        sys.exit(app.exec_())
    def buttonAddSeries_clicked(self):
        series = self.comboX.currentText()+","+self.comboY.currentText()+","+self.comboMarkerType.currentText()+","+self.comboMarkerColor.currentText()+","+self.lineEditMarkerSize.text()+","+self.comboLineStyle.currentText()+","+self.comboLineColor.currentText()+","+self.lineEditLineWidth.text()+","+self.comboTag.currentText()
        self.comboSeries.addItem(series)
        self.comboSeries.setCurrentIndex(self.comboSeries.count()-1)
    def buttonDeleteSeries_clicked(self):
        index = self.comboSeries.currentIndex()
        self.comboSeries.removeItem(index)
        self.comboSeries.setCurrentIndex(index-1)
    def buttonPlot_clicked(self):
        mpl.rcParams['figure.figsize'] = int(self.lineEditX.text()), int(self.lineEditY.text())
        mpl.rcParams['font.family'] = self.comboFont.currentText()
        mpl.rcParams['font.size'] = int(self.lineEditFontSize.text())
        mpl.rcParams['font.weight'] = self.comboWeight.currentText()
        mpl.rcParams['axes.linewidth'] = float(self.lineEditAxisLineWidth.text())
        mpl.rcParams['axes.titlesize'] = int(self.lineEditAxisTitleSize.text())
        mpl.rcParams['axes.labelsize'] = int(self.lineEditAxisLabelSize.text())

        NumOfLine = self.comboSeries.count()
        fig, ax = plt.subplots()
        for i in range(NumOfLine):
            Serieslist = self.comboSeries.itemText(i).split(',')
            sdata = self.data.sort_values(by=Serieslist[0])
            x = sdata[Serieslist[0]]
            y = sdata[Serieslist[1]]
            X = np.linspace(x.min(), x.max(), 201)
            model = interpolate.InterpolatedUnivariateSpline(x, y)
            Y = model(X)
            ax.plot(X, Y, marker=Serieslist[2], markerfacecolor=Serieslist[3], markersize=1,
                    linestyle=Serieslist[5], color=Serieslist[6], linewidth=int(Serieslist[7]),label=Serieslist[1])
            ax.scatter(x, y, marker=Serieslist[2], c=Serieslist[3], s=int(Serieslist[4]))
            if Serieslist[8] == "True":  # tag_name
                for x, y in zip(x, y):
                    ax.annotate("(%d,%d)" % (x, y), xy=(x, y), xytext=(-2, 5), textcoords='offset points',
                                fontsize=10, color=Serieslist[3])
        plt.xlabel(Serieslist[0])
        plt.ylabel("Concentration (ppm)")
        ax.legend(loc='upper right', shadow=True, fontsize='xx-small')
        plt.show()

app = QApplication(sys.argv)
ex = HW04Window()
ex.show()
sys.exit(app.exec_())