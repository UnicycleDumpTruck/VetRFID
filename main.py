#!/usr/bin/env python3
"""Application main code to run reader and display images."""
from __future__ import print_function
import sys
from time import sleep
import pyglet  # type: ignore
import scanner_window
import tag_dispatcher
import izar

# TODO Use argparse to set reader, reader power, window config, idle
# TODO Maybe have config file for defaults? idle, scanfreq, etc

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-m":
            print("Starting with mock reader...")
            sleep(1)
            reader = izar.MockReader()
        else:
            raise ValueError(f"Unknown command line argument: '{sys.argv[1]}'")
    else:
        print("Starting with hardware reader...")
        sleep(1)
        reader = izar.IzarReader('llrp://izar-51e4c8.local', protocol="GEN2")
        reader.set_read_plan([1, 2], "GEN2", read_power=1000)

    clock = pyglet.clock.get_default()

    display = pyglet.canvas.get_display()
    screens = display.get_screens()
    for i, screen in enumerate(screens):
        print(f"Screen #{i}: {screen}")
    # window2 = scanner_window.ScannerWindow(
    #       1920, 1080, "Pet U 2", True, fullscreen=True,
    #       screen=screens[1], window_number=2, antennas=[3,4])
    window1 = scanner_window.ScannerWindow(
        1920, 1080, "Pet U 1", True, fullscreen=True,
        screen=screens[0], window_number=1, antennas=[1,2])
    # window1 = scanner_window.ScannerWindow(
    #     1280, 720, "Pet U 1", True, window_number=1, antennas=[1, 2])
    # window2 = scanner_window.ScannerWindow(
    #     1280, 720, "Pet U 2", True, window_number=2, antennas=[3, 4])


    # event_logger1 = pyglet.window.event.WindowEventLogger()
    # window1.push_handlers(event_logger1)
    # event_logger2 = pyglet.window.event.WindowEventLogger()
    # window2.push_handlers(event_logger2)
    windows = { 
        window1: [1,2], 
        # window2: [2]
                }
    antennas = {'1': window1, 
                '2': window1, 
                # '3': window2, 
                # '4': window2
                }
    td = tag_dispatcher.TagDispatcher(reader, windows, antennas)

    clock = pyglet.clock.get_default()
    clock.schedule_interval(td.read_tags, 0.5)  # Called every 0.5 seconds

    pyglet.app.run()
