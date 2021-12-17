#!/usr/bin/env python3
from __future__ import print_function
# import mercury
import pyglet
import scanner_window
import tag_dispatcher
import izar


# reader = izar.mockReader()
reader = izar.izarReader('llrp://izar-51e4c8.local', protocol="GEN2")
clock = pyglet.clock.get_default()

# platform = pyglet.window.Window.get_platform()
display = pyglet.canvas.get_display()
screens = display.get_screens()
for screen in screens:
    print(screen)
window1 = scanner_window.ScannerWindow(900, 800, "Pet U 1", True, fullscreen=True, screen=screens[1], window_number=2)
window2 = scanner_window.ScannerWindow(900, 800, "Pet U 2", True, fullscreen=True, screen=screens[0], window_number=1)

# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

td = tag_dispatcher.TagDispatcher(reader, window1, window2)

clock = pyglet.clock.get_default()
clock.schedule_interval(td.read_tags, 0.5)  # Called every 0.5 seconds

pyglet.app.run()
