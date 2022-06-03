#!/usr/bin/env python3
"""Application main code to run reader and display images."""
from __future__ import print_function
from time import sleep
from os import environ
import sys
import argparse
from queue import Queue, Empty
from rich.traceback import install
from loguru import logger
import pyglet  # type: ignore
import scanner_window
import tag_dispatcher
import izar
from epc import Tag  # pylint: disable=unused-import

install(show_locals=True)

pyglet.options['search_local_libs'] = True
pyglet.options['debug_gl'] = False
pyglet.options['debug_gl_trace'] = False
pyglet.options['debug_gl_trace_args'] = False
pyglet.options['debug_lib'] = False
pyglet.options['debug_media'] = False
pyglet.options['debug_texture'] = False
pyglet.options['debug_trace'] = False
pyglet.options['debug_trace_args'] = False
pyglet.options['debug_trace_depth'] = 4


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add("main.log", rotation="1024 MB")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-background",
        help="Continuous read in backgroud process by Mercury API.",
        action="store_true"
    )
    parser.add_argument(
        "-poll",
        help="Poll read at intervals. Interferes with video playback.",
        action="store_true"
    )
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
            reader.set_read_plan([1, 2, 3, 4], "GEN2", read_power=args.power)
        else:
            reader.set_read_plan([1, 2, 3, 4], "GEN2", read_power=1600)

    idle_seconds = 3  # pylint: disable=invalid-name
    if args.idle:
        idle_seconds = args.idle

    environ["LD_LIBRARY_PATH"] = "/usr/bin/ffmpeg"

    clock = pyglet.clock.get_default()

    vet_paw = pyglet.image.load('media/icons/vet_u_paw.png')

    display = pyglet.canvas.get_display()
    screens = display.get_screens()
    for i, screen in enumerate(screens):
        print(f"Screen #{i}: {screen}")
    window2 = scanner_window.ScannerWindow(
          1920, 1080, "Ready Set Vet Screen 2", True, fullscreen=True,
          screen=screens[1], window_number=2, idle_seconds=idle_seconds)
    window1 = scanner_window.ScannerWindow(
        1920, 1080, "Ready Set Vet Screen 1", True, fullscreen=True,
        screen=screens[0], window_number=1, idle_seconds=idle_seconds)
    # window1 = scanner_window.ScannerWindow(
    #     1920, 1080, "Ready Set Vet", True, window_number=1, idle_seconds=idle_seconds)
    # window2 = scanner_window.ScannerWindow(
    #     1920, 1080, "Ready Set Vet", True, window_number=2, idle_seconds=idle_seconds)

    window1.set_icon(vet_paw)
    window2.set_icon(vet_paw)

    # event_logger1 = pyglet.window.event.WindowEventLogger()
    # window1.push_handlers(event_logger1)
    # event_logger2 = pyglet.window.event.WindowEventLogger()
    # window2.push_handlers(event_logger2)
    windows = {
        window2: [1, 2],
        window1: [3, 4]
    }
    antennas = {'1': window2,
                '2': window2,
                '3': window1,
                '4': window1
                }
    td = tag_dispatcher.TagDispatcher(
        reader, windows, antennas)  # type: ignore

    tag_queue: "Queue[Tag]" = Queue()

    def tag_to_queue(tag):
        """Put tag into queue."""
        if not tag_queue.full():
            logger.debug(f"{tag} going into queue from reading callback")
            tag_queue.put(tag, timeout=0.5)
        else:
            logger.warning("Queue full!")

    def not_read_queue():
        """Empty queue, return last item."""
        if not tag_queue.empty():
            last_tag = None
            while tag_queue.empty() is False:
                try:
                    tag = tag_queue.get(timeout=0.5)
                    logger.debug(tag)
                except Empty as ex:
                    logger.warning(f"read_queue exception:\n {ex}")
                    return None
                if tag is not None:
                    last_tag = tag
                else:
                    break
            return last_tag

    def read_queue():
        """Empty queue, return last item."""
        if tag_queue.empty():
            return
        contents = []
        logger.debug(f"Queue size: {tag_queue.qsize()}")
        # while not tag_queue.empty():
        for _ in range(tag_queue.qsize()):
            try:
                tag = tag_queue.get(timeout=0.5)
                contents.append(tag)
                logger.debug(
                    f"{tag} popped from queue. {tag_queue.qsize()} remaining.")
            except Empty as ex:
                logger.warning(f"read_queue exception:\n {ex}")
                # return None
            # else:
            #     break
        logger.debug(contents)
        return contents

    def send_tag_to_td(delta_time):  # pylint: disable=unused-argument
        """Send tag from the reader thread to the tag dispatcher."""
        if contents := read_queue():
            for tag in contents:
                logger.debug(f"Read tag: {tag}")
                td.tags_read(tag)
        else:
            logger.debug("Empty send_tag_to_td call!")

    def not_send_tag_to_td(delta_time):  # pylint: disable=unused-argument
        """Send tag from the reader thread to the tag dispatcher."""
        if tag := read_queue():
            logger.debug(f"Read tag: {tag}")
            td.tags_read(tag)
        else:
            logger.debug("Empty send_tag_to_td call!")

    clock = pyglet.clock.get_default()
    if args.poll:
        print("WARNING: Polled reading interferes with video playback!")
        sleep(3)
        clock.schedule_interval(td.read_tags, 0.5)  # Called every 0.5 seconds
        pyglet.app.run()
    else:
        reader.start_reading(on_time=500, callback=tag_to_queue)
        clock.schedule_interval(send_tag_to_td, 0.5)
        pyglet.app.run()
        reader.stop_reading()
