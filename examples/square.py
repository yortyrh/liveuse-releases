#!/usr/bin/env python3
"""Draw a small square with the LiveUse pointer.

Usage:
  python3 square.py
  python3 square.py /dev/cu.usbmodem1101

The port has to be the running sketch (USB 2886:802F), at 115200.
Opening it at 1200 baud sends the board into the bootloader.
"""

import sys
import time

import serial
from serial.tools import list_ports

VID = 0x2886
PID_RUNNING = 0x802F


def find_port():
    if len(sys.argv) > 1:
        return sys.argv[1]
    matches = [
        p.device
        for p in list_ports.comports()
        if p.vid == VID and p.pid == PID_RUNNING
    ]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        sys.exit(
            "No LiveUse found at 2886:802F. "
            "Pass the port: python3 square.py COM5"
        )
    sys.exit("More than one board. Pass the port: " + " ".join(matches))


def main():
    port = find_port()
    # 60 counts on a side. Positive x is right, positive y is down.
    lines = ("MOVE 60 0", "MOVE 0 60", "MOVE -60 0", "MOVE 0 -60")
    with serial.Serial(port, 115200, timeout=1) as link:
        time.sleep(0.3)
        link.reset_input_buffer()
        for line in lines:
            link.write((line + "\n").encode("ascii"))
            deadline = time.time() + 3
            while time.time() < deadline:
                reply = link.readline().decode("ascii", "replace").strip()
                if not reply:
                    continue
                print(reply)
                if reply.endswith("done"):
                    break


if __name__ == "__main__":
    main()
