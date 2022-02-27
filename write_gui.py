#!/usr/bin/env python3
"""Read and write tags in sets of two per item/animal number."""
from __future__ import print_function

import sys
from time import sleep

from loguru import logger
from PyQt5.QtCore import Qt
# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLineEdit, QMainWindow,
                             QPushButton, QComboBox, QVBoxLayout, QWidget)
from rich.traceback import install

import epc
import izar

install(show_locals=True)

reader = izar.MockReader()
#reader = izar.IzarReader("llrp://izar-51e4c8.local", protocol="GEN2")
#reader.set_read_plan([1], "GEN2")

# reader.set_read_plan([1], "GEN2", read_power=1500)
# reader.set_read_plan([1], "GEN2", read_power=1900)

NUM_TAGS_PER_SERIAL = 2


class PyCalcUi(QMainWindow):
    """PyCalc's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('PyCalc')
        self.setFixedSize(400, 400)
        # Set the central widget and the general layout
        self.general_layout = QVBoxLayout()
        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.general_layout)
        # Create the display and the buttons
        self._create_read_widget()
        self._create_write_widget()

    def _create_read_widget(self):
        """Create the display and button for reading a tag."""
        self.read_layout = QVBoxLayout()
        # Create the display widget
        self.read_display = QLineEdit()
        # Set some display's properties
        self.read_display.setFixedHeight(35)
        self.read_display.setAlignment(Qt.AlignRight)
        self.read_display.setReadOnly(True)
        # Add the display to the general layout
        self.read_layout.addWidget(self.read_display)
        self.read_display.setText("No tags read yet.")
        self.read_button = QPushButton("Read Tags")
        self.read_layout.addWidget(self.read_button)

        self.general_layout.addLayout(self.read_layout)

    def _create_write_widget(self):
        """Create the display and buttons for writing tags."""
        self.write_layout = QVBoxLayout()
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

        self.general_layout.addLayout(self.write_layout)

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
class PyCalcCtrl:
    """PyCalc Controller class."""

    def __init__(self, model, view):
        """Controller initializer."""
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connect_signals()

        self.serial_int = None
        with open("last_serial.txt", 'r', encoding="UTF8") as serial_file_in:
            self.serial_int = int(serial_file_in.readline().strip())

        self.next_tag = self._create_next_tag()

    def _read_tag(self):
        logger.info("Reading")
        tags_read = reader.read(timeout=100)
        logger.info(f"Tags read: {tags_read}")
        # self._view.read_display.setText(str(tags_read))
        self._view.read_display.setText("test")
        self._view.read_display.setFocus()
        return tags_read

    def _create_next_tag(self):
        """Generate next tag to write."""
        new_epc = epc.EpcCode("000000000000000000000000")
        new_epc.species_num = str(
            self._view.animal_selector.currentIndex())  # TODO remove str
        new_epc.serial = str(self.serial_int + 1)
        new_epc.location = str(self._view.position_selector.currentIndex())
        new_epc.date_now()
        if len(new_epc.code) != 24:
            raise ValueError(f"new_epc is wrong length: {new_epc}")
        self._view.serial_display.setText(new_epc.code)
        self._view.serial_display.setFocus()
        return new_epc

    def _write_tag(self):
        """Write tag with currently selected values."""
        logger.info("Writing...")
        print("writing...")
        tags_read = self._read_tag()
        sleep(0.5)
        if tags_read:
            self._view.read_display.setText(str(tags_read))
            self._view.read_display.setFocus()
            # TODO set target to closest by RSSI
            target_tag = tags_read[0]
            # print("Targeted tag", target_tag)

            old = target_tag.epc.epc_bytes
            new = self.next_tag.epc_bytes
            if reader.write(epc_code=new, epc_target=old):
                print(f'Rewrote {old}\nwith    {new}')
                print("Label your tag:", self.next_tag.species_string, end=", ")
                print("Head" if self._view.position_selector.currentIndex() ==
                      1 else "Tail", end=", ")
                print(self._view.next_serial)

                # Increment counters after successful write
                if self._view.position_selector.currentIndex() == 1:
                    self._view.serial_int = self.increment_serial(
                        self._view.serial_int)
                    self._view.position_selector.setIndex(1)
                else:
                    self._view.position_selector.setIndex(1)

            else:
                print('No tag found')

    def increment_serial(self, s_int):
        """Given an integer, write it to file tracking last serial number used."""
        if s_int is None:
            raise ValueError("Serial number can't be None.")
        s_int += 1
        with open('last_serial.txt', 'w', encoding='UTF8') as serial_file_out:
            serial_file_out.write(str(s_int))
        return s_int

    def _calculate_result(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _connect_signals(self):
        """Connect signals and slots."""
        self._view.read_button.clicked.connect(self._read_tag)
        self._view.serial_display.returnPressed.connect(self._calculate_result)
        self._view.write_button.clicked.connect(self._write_tag)


# Create a Model to handle the calculator's operation
def evaluate_expression(expression):
    """Evaluate an expression."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception as ex:
        result = "ERROR_MSG"
        logger.warning(ex)

    return result


def main():
    """Main function."""

    # tag_position: int = 1  # pylint: disable=invalid-name

    # Create an instance of QApplication
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = PyCalcUi()
    view.show()
    # Create instances of the model and the controller
    model = evaluate_expression
    PyCalcCtrl(model=model, view=view)
    # Execute the calculator's main loop
    sys.exit(pycalc.exec())


if __name__ == '__main__':
    main()
