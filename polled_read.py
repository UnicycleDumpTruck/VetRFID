#!/usr/bin/env python3
from __future__ import print_function
import mercury
import pyglet
import scanner_window
import tag_dispatcher


reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")
print(reader.get_model())
reader.set_read_plan([1, 2], "GEN2", read_power=1500)

clock = pyglet.clock.get_default()

window = scanner_window.ScannerWindow(900, 800, "Pet U", True)
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

td = tag_dispatcher.TagDispatcher(reader, window)

clock = pyglet.clock.get_default()
clock.schedule_interval(td.read_tags, 0.1)  # Called every 0.1 seconds

pyglet.app.run()
