#!/usr/bin/env python3
"""Read and write tags in sets of two per item/animal number."""
from __future__ import print_function

import sys
from time import sleep

from loguru import logger
from PyQt5.QtCore import Qt, QObject  # pylint: disable=no-name-in-module
# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QLabel, QFrame,  # pylint: disable=no-name-in-module
                             QPushButton, QComboBox, QVBoxLayout, QWidget, QHBoxLayout)   # pylint: disable=no-name-in-module
from PyQt5.QtGui import (QPixmap)
from rich.traceback import install

import epc
import izar

install(show_locals=True)

reader = izar.MockReader()
# reader = izar.IzarReader("llrp://izar-51e4c8.local", protocol="GEN2")
# reader.set_read_plan([1], "GEN2")

# reader.set_read_plan([1], "GEN2", read_power=1500)
# reader.set_read_plan([1], "GEN2", read_power=1900)

NUM_TAGS_PER_SERIAL = 2


class FramedWidget(QFrame):
    """Widget with a frame around it."""

    def __init__(self, *args):
        super(FramedWidget, self).__init__(*args)
        # self.setStyleSheet(
        #     "background-color: rgb(255,255,255); margin:5px; border:2px solid rgb(0, 255, 0); ")


class PyCalcUi(QMainWindow):
    """PyCalc's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('PyCalc')
        # self.setFixedSize(500, 500)
        # Set the central widget and the general layout
        self.general_layout = QVBoxLayout()
        self._central_widget = FramedWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.general_layout)
        # Create the display and the buttons
        self._create_title_widget()
        self._create_read_widget()
        self._create_write_widget()
        self._create_log_widget()

    def _create_title_widget(self):
        self.title_widget = QWidget()
        self.title_layout = QHBoxLayout(self.title_widget)
        self.logo_widget = QLabel()
        self.logo = QPixmap('media/icons/vet_u_paw.png').scaledToHeight(150)
        self.logo_widget.setPixmap(self.logo)
        self.title_layout.addWidget(self.logo_widget)
        self.title_layout.addSpacing(20)
        self.title_label = QLabel("Read Set Vet RFID", self.title_widget)
        self.title_label.setAlignment(Qt.AlignVCenter)
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        self.general_layout.addWidget(self.title_widget)

    def _create_read_widget(self):
        """Create the display and button for reading a tag."""
        self.read_widget = QWidget()
        self.read_layout = QVBoxLayout(self.read_widget)
        self.read_label = QLabel("Tags read:", self.read_widget)
        self.read_layout.addWidget(self.read_label)
        # Create the display widget
        self.read_display = QLineEdit()
        self.read_label.setBuddy(self.read_display)
        # Set some display's properties
        self.read_display.setFixedHeight(35)
        self.read_display.setAlignment(Qt.AlignRight)
        self.read_display.setReadOnly(True)
        # Add the display to the general layout
        self.read_layout.addWidget(self.read_display)
        self.read_display.setText("No tags read yet.")
        self.read_button = QPushButton("Read Tags")
        self.read_layout.addWidget(self.read_button)
        self.general_layout.addWidget(self.read_widget)
        # self.general_layout.addLayout(self.read_layout)

    def _create_write_widget(self):
        """Create the display and buttons for writing tags."""
        self.write_widget = QWidget()
        self.write_layout = QVBoxLayout(self.write_widget)
        self.write_label = QLabel("Next tag to write:", self.write_widget)
        self.write_layout.addWidget(self.write_label)
        self.write_label.setMinimumSize(200, 50)
        self.serial_display = QLineEdit()
        self.serial_display.setFixedHeight(35)
        self.serial_display.setAlignment(Qt.AlignRight)
        self.serial_display.setReadOnly(True)
        self.write_layout.addWidget(self.serial_display)
        # self.set_display_text(str(self.serial_int + 1))

        self.animal_selector = QComboBox()
        self.animal_selector.addItems(epc.species_names.values())
        self.write_layout.addWidget(self.animal_selector)

        self.position_selector = QComboBox()
        self.position_selector.addItems(["Head", "Tail"])
        self.write_layout.addWidget(self.position_selector)

        self.write_button = QPushButton("Write Tag")
        # write_button.setFixedSize(100,100)
        self.write_layout.addWidget(self.write_button)
        self.general_layout.addWidget(self.write_widget)
        # self.general_layout.addLayout(self.write_layout)

    def _create_log_widget(self):
        """Create area for tag data just written."""
        self.log_widget = QWidget()
        self.log_layout = QVBoxLayout(self.log_widget)
        self.log_label = QLabel("Log:", self.log_widget)
        self.log_layout.addWidget(self.log_label)
        self.log_display = QLineEdit()
        self.log_display.setFixedHeight(70)
        self.log_display.setAlignment(Qt.AlignCenter)
        self.log_display.setReadOnly(True)
        self.log_layout.addWidget(self.log_display)
        self.general_layout.addWidget(self.log_widget)
        # self.general_layout.addLayout(self.log_layout)

    def set_display_text(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def display_text(self):
        """Get display's text."""
        return self.display.text()

    def clear_display(self):
        """Clear the display."""
        self.set_display_text('')

# Create a controller class to connect the GUI and the model


class PyCalcCtrl(QObject):
    """PyCalc Controller class."""

    def __init__(self, model, view):
        """Controller initializer."""
        super().__init__()
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connect_signals()

        self.serial_int = None
        with open("last_serial.txt", 'r', encoding="UTF8") as serial_file_in:
            self.serial_int = int(serial_file_in.readline().strip())

        self.next_tag = self._create_next_tag()

    # @pyqtSlot()
    def _read_tag(self):
        logger.debug("Reading")
        tags_read = reader.read(timeout=100)
        logger.info(f"Tags read: {tags_read}")
        # self._view.read_display.setText(str(tags_read))
        if tags_read:
            self._view.read_display.setText(tags_read[0])
            self._view.log_display.setText(f"Read: {str(tags_read)}")
        else:
            self._view.read_display.setText("Read: None")
            self._view.log_display.setText(f"Read: None")
        self._view.read_display.setFocus()
        return tags_read

    # @pyqtSlot(name='_create_next_tag')
    def _create_next_tag(self):
        """Generate next tag to write."""
        new_epc = epc.EpcCode("000000000000000000000000")
        new_epc.species_num = str(
            self._view.animal_selector.currentIndex() + 1)  # TODO remove str?
        new_epc.serial = str(self.serial_int + 1)
        new_epc.location = str(self._view.position_selector.currentIndex() + 1)
        new_epc.date_now()
        if len(new_epc.code) != 24:
            raise ValueError(f"new_epc is wrong length: {new_epc}")
        self._view.serial_display.setText(new_epc.code)
        self._view.serial_display.setFocus()
        return new_epc

    # @pyqtSlot(name='_write_tag')
    def _write_tag(self):
        """Write tag with currently selected values."""
        tags_read = self._read_tag()
        sleep(0.5)
        if tags_read:
            self._view.read_display.setText(str(tags_read))
            self._view.read_display.setFocus()
            # TODO set target to closest by RSSI
            target_tag = tags_read[0]

            old = target_tag.epc.epc_bytes
            new = self.next_tag.epc_bytes
            if reader.write(epc_code=new, epc_target=old):
                logger.info(f'Rewrote {old} with {new}')
                animal = self.next_tag.species_string
                loc = self._view.position_selector.currentText()
                ser = self._view.next_serial
                log_str = f"Success: Label your tag: {animal} {loc} {ser}"
                self._view.log_display.setText(log_str)
                logger.debug(log_str)

                # Increment counters after successful write
                if self._view.position_selector.currentIndex() == 1:
                    self._view.increment_serial()
                    self._view.position_selector.setIndex(1)
                else:
                    self._view.position_selector.setIndex(1)

            else:
                self._view.log_display.setText("Error: Write failed.")
                logger.warning("Write failed.")
        else:
            self._view.log_display.setText(
                "Error: Can't write, no tag detected.")
            logger.warning("Can't write, no tag detected.")

    def increment_serial(self):
        """Given an integer, write it to file tracking last serial number used."""
        self.serial_int += 1
        with open('last_serial.txt', 'w', encoding='UTF8') as serial_file_out:
            serial_file_out.write(str(self.serial_int))

    def _connect_signals(self):
        """Connect signals and slots."""
        self._view.read_button.clicked.connect(self._read_tag)
        # self._view.serial_display.returnPressed.connect(self._calculate_result)
        self._view.write_button.clicked.connect(self._write_tag)

        self._view.animal_selector.currentIndexChanged.connect(
            self._create_next_tag)
        self._view.position_selector.currentIndexChanged.connect(
            self._create_next_tag)


def placeholder_model():
    """Still working on the full MVC paradigm for this app."""


def main():
    """Main function."""
    # Create an instance of QApplication
    pycalc = QApplication(sys.argv)
    # Show the GUI
    view = PyCalcUi()
    view.show()
    # Create instances of the model and the controller
    model = placeholder_model

    # assigning to ctrllr fixed signals, tho ctrllr not used
    ctrllr = PyCalcCtrl(model=model, view=view)

    # Execute the main loop
    sys.exit(pycalc.exec())


if __name__ == '__main__':
    main()
