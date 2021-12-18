#!/usr/bin/env python3
from __future__ import print_function
# import mercury
import pyglet
import scanner_window
import tag_dispatcher
import izar


reader = izar.mockReader()
# reader = izar.izarReader('llrp://izar-51e4c8.local', protocol="GEN2")
clock = pyglet.clock.get_default()

display = pyglet.canvas.get_display()
screens = display.get_screens()
for screen in screens:
    print(screen)
# window1 = scanner_window.ScannerWindow(900, 800, "Pet U 2", True, fullscreen=True, screen=screens[1], window_number=2, antennas=[1])
# window2 = scanner_window.ScannerWindow(900, 800, "Pet U 1", True, fullscreen=True, screen=screens[0], window_number=1, antennas=[2])
window1 = scanner_window.ScannerWindow(
    900, 800, "Pet U 2", True, window_number=2, antennas=[2])
window2 = scanner_window.ScannerWindow(
    900, 800, "Pet U 1", True, window_number=1, antennas=[1])

# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)
windows = {window1: [1], window2: [2]}
antennas = {'1': window1, '2': window2}
td = tag_dispatcher.TagDispatcher(reader, windows, antennas)

clock = pyglet.clock.get_default()
clock.schedule_interval(td.read_tags, 0.5)  # Called every 0.5 seconds

pyglet.app.run()
