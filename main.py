#!/usr/bin/env python3
"""Application main code to run reader and display images."""
from __future__ import print_function
from time import sleep
from os import environ
import argparse
import pyglet  # type: ignore
import scanner_window
import tag_dispatcher
import izar


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-mock",
        help="Run with mock reader, keys p and d send tags.",
        action="store_true"
    )
    parser.add_argument(
        "-idle",
        type=int,
        help="Number of seconds before window idles."
    )
    parser.add_argument(
        "-power",
        type=int,
        choices=range(0, 3150),
        metavar="[0-3150]",
        help="Power level of RFID tag reader in centidBm, 0-3150"
    )

    args = parser.parse_args()

    if args.mock:
        print("Starting with mock reader...")
        sleep(1)
        reader = izar.MockReader()
    else:
        print("Starting with hardware reader...")
        sleep(1)
        reader = izar.IzarReader('llrp://izar-51e4c8.local', protocol="GEN2")
        if args.power:
            reader.set_read_plan([1, 2], "GEN2", read_power=args.power)
        else:
            reader.set_read_plan([1, 2], "GEN2", read_power=1000)

    idle_seconds = 3  # pylint: disable=invalid-name
    if args.idle:
        idle_seconds = args.idle

    environ["LD_LIBRARY_PATH"] = "/usr/bin/ffmpeg"
    
    clock = pyglet.clock.get_default()

    display = pyglet.canvas.get_display()
    screens = display.get_screens()
    for i, screen in enumerate(screens):
        print(f"Screen #{i}: {screen}")
    # window2 = scanner_window.ScannerWindow(
    #       1920, 1080, "Pet U 2", True, fullscreen=True,
    #       screen=screens[1], window_number=2, idle_seconds=idle_seconds)
    # window1 = scanner_window.ScannerWindow(
    #     1920, 1080, "Pet U 1", True, fullscreen=True,
    #     screen=screens[0], window_number=1, idle_seconds=idle_seconds)
    window1 = scanner_window.ScannerWindow(
        1280, 720, "Pet U 1", True, window_number=1, idle_seconds=idle_seconds)
    # window2 = scanner_window.ScannerWindow(
    #     1280, 720, "Pet U 2", True, window_number=2, idle_seconds=idle_seconds)

    # event_logger1 = pyglet.window.event.WindowEventLogger()
    # window1.push_handlers(event_logger1)
    # event_logger2 = pyglet.window.event.WindowEventLogger()
    # window2.push_handlers(event_logger2)
    windows = {
        window1: [1, 2],
        # window2: [3, 4]
    }
    antennas = {'1': window1,
                '2': window1,
                # '3': window2,
                # '4': window2
                }
    td = tag_dispatcher.TagDispatcher(
        reader, windows, antennas)  # type: ignore

    clock = pyglet.clock.get_default()
    clock.schedule_interval(td.read_tags, 0.5)  # Called every 0.5 seconds
    clock.schedule_interval(window1.update, 1/30.0)
    pyglet.app.run()
