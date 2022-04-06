from PyQt5.QtWidgets import \
        QWidget, QPushButton, QGridLayout, \
        QLabel, QLineEdit, QComboBox,  \
        QTableWidget, QTableWidgetItem, QVBoxLayout, \
        QHBoxLayout, QFrame, QFileDialog, \
        QStackedWidget, QHeaderView

from PyQt5.QtCore import Qt, QTimer
import shutil
from datetime import datetime

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("RingSaver")

        with open("button.qss", 'r') as infile:
            buttonStyle = infile.read()
        self.buttonSpace = QHBoxLayout(self)
        self.bodySpace   = QVBoxLayout(self)
        
        self.fileToSave = None
        self.backupLocation = None

        # Choose file to backup
        backupFileButton     = QPushButton("Choose File To Backup", self)
        backupFileButton.clicked.connect(self.getBackedFile)
        backupFileButton.setStyleSheet(buttonStyle)

        backupFileText   = QLineEdit("")
        
        # Choose backup location
        backupLocButton = QPushButton("Choose Backup Location", self)
        backupLocButton.clicked.connect(self.getBackedLoc)
        backupLocText = QLineEdit("")
        backupLocButton.setStyleSheet(buttonStyle)

        # Backup Timer
        self.backupIntervalText = QLineEdit("")
        self.backupIntervalUnits = QComboBox()
        self.backupIntervalUnits.addItems(
            [
                "seconds",
                "minutes",
                "hours",
                "days"
            ]
        )

        backupIntervalButton = TimerButton(self)
        

        # Log window
        self.entries = 0
        self.logTable = QTableWidget(0, 2, self)
        self.logTable.horizontalHeader().setStretchLastSection(True)
        self.logTable.setHorizontalHeaderLabels(['Time', "Message"])
        self.logTable.verticalHeader().setVisible(False)
        self.logTable.setTextElideMode(Qt.ElideRight)
        self.logTable.setWordWrap(True)

        # Options
        optionsButton = QPushButton("Options", self)
        optionsButton.clicked.connect(self.openOptions)
        optionsButton.setStyleSheet(buttonStyle)

        # Start Button
        startButton = QPushButton("Start", self)
        startButton.clicked.connect(self.createTimer)
        startButton.setStyleSheet(buttonStyle)
        
        self.cTimer = None

        # row, column, height, width             r, c, h, w 
        self.buttonSpace.addWidget(backupFileButton)
        self.buttonSpace.addWidget(backupLocButton)
        self.buttonSpace.addWidget(backupIntervalButton)
        self.buttonSpace.addWidget(optionsButton)
        self.buttonSpace.addWidget(startButton)

        # self.grid.addWidget()
        # self.grid.addWidget()
        # self.grid.addWidget()
        fakeWidget = QWidget(self)
        fakeWidget.setLayout(self.buttonSpace)
        self.bodySpace.addWidget(fakeWidget)

        self.bodySpace.addWidget(self.logTable)

        backupIntervalButton.logTable = self.logTable
        self.backupIntervalButton = backupIntervalButton
        self.setLayout(self.bodySpace)

    def openOptions(self):
        pass

    def getBackedFile(self):
        fileToSave = QFileDialog.getOpenFileName(self)
        fileToSave = fileToSave[0]
        print(fileToSave)
        if len(fileToSave) > 0:
            self.fileToSave = fileToSave
        self.addLogItem("Selected:\n{}".format(fileToSave))
        print("Selected:\n{}".format(fileToSave))

    def getBackedLoc(self):
        backupLocation = QFileDialog.getExistingDirectory(self)
        if len(backupLocation) > 0:
            self.backupLocation = backupLocation
        self.addLogItem("Backup To:\n{}".format(backupLocation))
        print(backupLocation)

    def setNewTimer(self):
        interval = self.backupIntervalText.text()
        if interval.isnumeric():
            interval = int(interval)
        else:
            print("Not a valid integer: {}".format(interval))
            return
        units    = self.backupIntervalUnits.currentText()
        print("Backup every {} {}".format(interval, units))
        pass
    
    def addLogItem(self, message, insertAt=0):
        messageWidget = QTableWidgetItem(message)
        messageWidget.setFlags(messageWidget.flags() & ~Qt.ItemIsEditable)
        cTime = QTableWidgetItem(self.getCurrentTimeAsString())
        cTime.setFlags(cTime.flags() & ~Qt.ItemIsEditable)
        self.logTable.insertRow(insertAt)
        self.logTable.setItem(insertAt, 0, cTime)
        self.logTable.setItem(insertAt, 1, messageWidget)
        self.logTable.resizeRowsToContents()
        if self.logTable.rowCount() == 1:
            # self.logTable.horizontalHeader().ResizeMode(0, QHeaderView.ResizeToContents)
            self.logTable.resizeColumnToContents(0)
    
    def backupFile(self):
        if          self.fileToSave is not None and len(self.fileToSave) > 0 \
            and self.backupLocation is not None and len(self.backupLocation) > 0:
            cTime = self.getCurrentTimeAsString()
            newBackup = "{}/{}.{}.bak".format(self.backupLocation, self.fileToSave.split("/")[-1], cTime)
            self.addLogItem("Backing up \n{}\nas\n{}".format(self.fileToSave, newBackup))
            import pathlib
            firstFile = pathlib.Path(self.fileToSave)
            # print(firstFile)
            # print(firstFile.is_file())
            secondFile = pathlib.Path(newBackup)
            # print(secondFile)
            # RUN COPY
            shutil.copy2(firstFile, secondFile)

    def getCurrentTimeAsString(self):
        return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def createTimer(self):
        if self.cTimer is not None:
            # Stop timer
            self.cTimer.stop()
            self.addLogItem("Previous timer stopped.")
            # Set to null
            self.cTimer = None
        # Check that we have a valid time interval for a timer
        milliseconds = self.backupIntervalButton.getMilliseconds()
        if milliseconds is None:
            self.addLogItem("Valid backup interval not specified.")
            return
        if self.fileToSave is None or len(self.fileToSave) == 0:
            self.addLogItem("No valid file to backup has been specified.")
            return
        if self.backupLocation is None or len(self.backupLocation) == 0:
            self.addLogItem("No valid backup location has been specified.")
            return
        # Create the timer
        self.addLogItem("Backup started.")
        self.backupFile()
        self.cTimer = QTimer()
        # Link it to the backup function
        self.cTimer.timeout.connect(self.backupFile)
        self.cTimer.start(milliseconds)


class TimerButton(QStackedWidget):
    def __init__(self, parent=None, log=None):
        self.logTable = log
        super(TimerButton, self).__init__(parent)
        dummyWidget1 = QWidget(self)
        self.layoutButton = QVBoxLayout(dummyWidget1)


        self.intervalLabel = QLabel("", dummyWidget1)
        self.intervalLabel.setAlignment(Qt.AlignCenter)
        self.layoutButton.addWidget(self.intervalLabel)

        firstButton = QPushButton("Timer")
        self.layoutButton.addWidget(firstButton)

        self.unitsLabel = QLabel("", dummyWidget1)
        self.unitsLabel.setAlignment(Qt.AlignCenter)
        self.layoutButton.addWidget(self.unitsLabel)
        dummyWidget1.setLayout(self.layoutButton)

        dummyWidget2 = QWidget(self)
        self.layoutTimer = QVBoxLayout(dummyWidget2)
        self.units = QComboBox()
        self.units.addItems([
            "seconds",
            "minutes",
            "hours",
            "days"
            ])

        self.intervalText = QLineEdit("", self)
        acceptButton = QPushButton("Accept", self)

        self.layoutTimer.addWidget(self.intervalText)
        self.layoutTimer.addWidget(self.units)
        self.layoutTimer.addWidget(acceptButton)
        dummyWidget2.setLayout(self.layoutTimer)

        self.addWidget(dummyWidget1)
        self.addWidget(dummyWidget2)
        firstButton.clicked.connect(self.switchLayout)
        acceptButton.clicked.connect(self.switchLayout)
        self.firstLayout = True 
        print(self.widget(0))
        print(self.widget(1))
        self.widget(0).show()

    def switchLayout(self):
        if self.firstLayout:
            self.setCurrentWidget(self.widget(1))
        else:
            tyme  = self.intervalText.text()
            units = self.units.currentText()
            self.intervalLabel.setText(tyme)
            self.unitsLabel.setText(units)
            self.addLogItem("Backing up every:\n{} {}".format(tyme, units))
            self.setCurrentWidget(self.widget(0))

        self.firstLayout = not self.firstLayout

    def getUnits(self):
        return self.units.currentText()

    def getInterval(self):
        return self.intervalText.text()

    def addLogItem(self, message, insertAt=0):
        if self.logTable is not None:
            messageWidget = QTableWidgetItem(message)
            messageWidget.setFlags(messageWidget.flags() & ~Qt.ItemIsEditable)
            cTime = QTableWidgetItem(self.getCurrentTimeAsString())
            cTime.setFlags(cTime.flags() & ~Qt.ItemIsEditable)
            self.logTable.insertRow(insertAt)
            self.logTable.setItem(insertAt, 0, cTime)
            self.logTable.setItem(insertAt, 1, messageWidget)
            self.logTable.resizeRowsToContents()
            if self.logTable.rowCount() == 1:
                # self.logTable.horizontalHeader().ResizeMode(0, QHeaderView.ResizeToContents)
                self.logTable.resizeColumnToContents(0)
     
    def getMilliseconds(self):
        units = self.getUnits()
        tyme = self.getInterval()
        if len(tyme) < 0 or not tyme.isnumeric():
            return None
        conversion = {
            'seconds': 1000,
            "minutes": 1000*60,
            "hours":   1000*60*60,
            "days":    1000*60*60*24
        }
        tyme = int(tyme)
        if tyme <= 0:
            return None
        return tyme * conversion[units]

    def getCurrentTimeAsString(self):
        return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
