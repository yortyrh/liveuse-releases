<p align="center">
  <img src="assets/logo.png" width="128" height="128" alt="LiveUse">
</p>

<h1 align="center">LiveUse</h1>

<p align="center">
  <a href="https://github.com/yortyrh/liveuse-releases/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/yortyrh/liveuse-releases?label=firmware"></a>
</p>

<p align="center">
  Binaries for a Seeed Studio XIAO SAMD21.<br>
  One USB Type-C cable makes the computer see a mouse, a keyboard, and a serial port.
</p>

This repository publishes the compiled firmware. Each version is a [release](https://github.com/yortyrh/liveuse-releases/releases). The `main` branch holds the latest [`manifest.json`](manifest.json). The binaries are release assets, and they download without a token: the repository stays public for that reason.

The firmware published today is **0.5.0**. Once flashed, the board announces manufacturer `LiveUse` and product `LiveUse 0.5.0`. The mouse is `LiveUse Mouse 0.5.0` and the keyboard is `LiveUse Keyboard 0.5.0`.

## The board

The binary in this repository is built for the **Seeed Studio XIAO SAMD21**, the board previously sold as **Seeeduino XIAO**.

| | |
|---|---|
| Microcontroller | Microchip **ATSAMD21G18A**, Arm Cortex-M0+ at 48 MHz |
| Flash / RAM | 256 KB / 32 KB |
| USB | VID `0x2886` (Seeed) |
| Running sketch | PID `0x802F`. The host shows it as LiveUse |
| SAM-BA bootloader | PID `0x002F`. The host shows it as Seeeduino XIAO |

Use a USB Type-C cable that carries data. A charge-only cable powers the board and leaves it invisible to the computer.

Search for a board whose name includes **SAMD21** or **Seeeduino XIAO**. Seeed also sells XIAO boards with a different microcontroller (ESP32-S3, RP2040, nRF52840). Those boards need a different image and a different bootloader. The XIAO SAMD21 Plus uses the same chip; the image here is built for the original XIAO SAMD21.

### Where to buy one

- On Amazon, search for [Seeed Studio XIAO SAMD21](https://www.amazon.com/s?k=Seeed+Studio+XIAO+SAMD21). The same words work on your local Amazon (`amazon.es`, `amazon.com.mx`, and the rest).
- Seeed's store: [Seeed Studio XIAO SAMD21](https://www.seeedstudio.com/Seeeduino-XIAO-Arduino-Microcontroller-SAMD21-Cortex-M0+-p-4426.html).
- The board guide, with the pinout and the bootloader gesture: [Seeed's wiki](https://wiki.seeedstudio.com/Seeeduino-XIAO/).

## Download the binary

Flash the version named in [`manifest.json`](https://raw.githubusercontent.com/yortyrh/liveuse-releases/main/manifest.json) on `main`. That file has the asset name, the URL, the SHA-256, the size, and the write offset.

The 0.5.0 image for this board is:

[liveuse-seeed_xiao-0.5.0.bin](https://github.com/yortyrh/liveuse-releases/releases/download/firmware-v0.5.0/liveuse-seeed_xiao-0.5.0.bin)

```sh
curl -fL -o liveuse-seeed_xiao-0.5.0.bin \
  https://github.com/yortyrh/liveuse-releases/releases/download/firmware-v0.5.0/liveuse-seeed_xiao-0.5.0.bin
```

Check the SHA-256 against the `sha256` field in the manifest:

```sh
# macOS
shasum -a 256 liveuse-seeed_xiao-0.5.0.bin

# Linux
sha256sum liveuse-seeed_xiao-0.5.0.bin

# Windows
certutil -hashfile liveuse-seeed_xiao-0.5.0.bin SHA256
```

The 0.5.0 digest is `55f8e81d0b6baa2ccbcf2338f0658cdf1327deb9f253b3dffe0e502a02147a2f` (38872 bytes).

## Flash

The `.bin` file is the application, and it starts at address **`0x2000`**. The first 8 KB are the factory bootloader. Leave them in place.

Close any program that has the serial port open (a serial monitor, a script, the Chrome page below). The port cannot be shared.

### Enter the bootloader

On the original XIAO SAMD21, two pads are marked **RST**. With the board plugged in, short them **twice** in a row, with tweezers or a short piece of wire. The orange LED flickers and stays lit, and a new serial port appears. The USB id is then `2886:002F`.

On the XIAO SAMD21 Plus, press the Reset button twice.

When the board is already running LiveUse, opening its CDC port at **1200** baud and closing it also enters the bootloader. Talk to the firmware at **115200**. Opening the port at 1200 reboots the board into the bootloader.

Wait a couple of seconds for the new port to settle. On macOS the name changes (`cu.usbmodem1101` can become `cu.usbmodem1102`). Use the port that appeared after the double reset.

| System | How to list the port |
|---|---|
| macOS | `ls /dev/cu.usb*` |
| Linux | `ls /dev/ttyACM*` |
| Windows | Device Manager, or `pio device list` |
| Either | Arduino IDE → Tools → Port |

If the write stops halfway, wait two seconds and run the same command again, while the LED is still in bootloader mode.

### PlatformIO

PlatformIO ships **bossac 1.7**. That version keeps the 8 KB bootloader when it erases. Use the command below with that bossac. Version 1.7 has no `--offset` flag.

Install the [PlatformIO CLI](https://platformio.org/install/cli). In an empty folder, create `platformio.ini` so PlatformIO downloads the tool:

```ini
[env:seeed_xiao]
platform = atmelsam
board = seeed_xiao
framework = arduino
```

```sh
pio pkg install
```

The tool lands here:

| System | bossac |
|---|---|
| macOS and Linux | `~/.platformio/packages/tool-bossac/bossac` |
| Windows | `%USERPROFILE%\.platformio\packages\tool-bossac\bossac.exe` |

Confirm that `--help` says `Version 1.7.0`. Then, with the board in the bootloader:

```sh
# macOS. The name is the one under /dev, without the directory.
~/.platformio/packages/tool-bossac/bossac \
  --port=cu.usbmodem1101 --erase --write --verify --reset -U true \
  liveuse-seeed_xiao-0.5.0.bin

# Linux
~/.platformio/packages/tool-bossac/bossac \
  --port=ttyACM0 --erase --write --verify --reset -U true \
  liveuse-seeed_xiao-0.5.0.bin

# Windows
%USERPROFILE%\.platformio\packages\tool-bossac\bossac.exe ^
  --port=COM5 --erase --write --verify --reset -U true ^
  liveuse-seeed_xiao-0.5.0.bin
```

Replace the port with the one that appeared after the double reset. This PlatformIO folder does not compile LiveUse. It only puts bossac on disk so you can write the `.bin` from this repository.

### Arduino IDE

The IDE does two jobs: it installs Seeed's bossac, and afterwards it opens the serial monitor. The `.bin` from this repository is written with bossac, the same way as above.

1. Install the [Arduino IDE](https://www.arduino.cc/en/software).
2. File → Preferences → *Additional boards manager URLs*:

   ```
   https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json
   ```

3. Tools → Board → Boards Manager. Search for **Seeed Studio XIAO SAMD21** and install **Seeed SAMD Boards**.
4. Find the `bossac` you just installed and read it with `--help`:

   ```sh
   # macOS
   find ~/Library/Arduino15/packages/Seeeduino/tools -name bossac -type f

   # Linux
   find ~/.arduino15/packages/Seeeduino/tools -name bossac -type f
   ```

   On Windows, search for `bossac.exe` under `%LOCALAPPDATA%\Arduino15\packages\Seeeduino\tools`.

5. When that help text says **1.7**, use the same command as PlatformIO (`--erase --write --verify --reset -U true`), with no `--offset`.
6. When the help text lists **`--offset`** (bossac 1.8 or 1.9), pass it. Otherwise bossac writes at `0x0` and erases the bootloader:

   ```sh
   bossac --port=cu.usbmodem1101 -U --offset=0x2000 \
     --erase --write --verify --reset \
     liveuse-seeed_xiao-0.5.0.bin
   ```

When bossac finishes, the board resets on its own. USB returns to `2886:802F` and the product name becomes `LiveUse`, with the version from the binary.

## Check that it answers

Open the sketch port at **115200** baud, 8 data bits, no parity, one stop bit. When the port opens (the host raises DTR) the board prints:

```
=== LiveUse ===
USB: composite HID mouse + keyboard + CDC serial
Motion: MOVE glides in small steps
================
Commands (line-oriented, LF/CRLF):
  ...
```

In the Arduino IDE: Tools → Serial Monitor, 115200, line ending **Newline**. Type `STATUS` and press Enter. The reply looks like:

```
OK uptime_ms=18420 fw=0.5.0
```

`fw=` is the version on the board. Then try a short move, with the pointer in view:

```
MOVE 80 0
```

The board answers `MOVE 80 0` and, when the glide finishes, `MOVE done`. The pointer moves right.

On macOS or Linux, the terminal works too. The port name is the sketch port, already at PID `0x802F`:

```sh
# macOS
screen /dev/cu.usbmodem1101 115200

# Linux
screen /dev/ttyACM0 115200
```

Leave `screen` with `Ctrl-A` then `K`.

## Commands

One line, one command. The line ends in LF or CRLF; CR is ignored. The command word is case-insensitive. For the keyboard commands, the text after the word keeps its case.

Each `MOVE` axis, and the step count of `SCROLL` and `HSCROLL`, is clamped to **±2000**. A line longer than **95** characters does not run and answers `ERR line too long`. Mouse and keyboard commands block the port until the gesture finishes: the next line is read after that.

A line that is not a command comes back as `ECHO` plus the text. That is a way to check that the port is alive.

The keyboard types into whichever window has focus. To try `TYPE` and `KEY`, leave an empty editor in front.

| Command | What it does | Reply |
|---|---|---|
| `HELP` or `?` | List the commands | The help text |
| `STATUS` | Uptime and version | `OK uptime_ms=<ms> fw=<version>` |
| `ECHO <text>` | Send the text back | `ECHO <text>` |
| `MOVE <dx> <dy>` | Glide the pointer in a straight line, in small steps. Positive `dx` is right, positive `dy` is down | `MOVE <dx> <dy>` and then `MOVE done` |
| `CLICK left` | Left click | `CLICK left` and `CLICK left done` |
| `CLICK right` | Right click | The same, with `right` |
| `CLICK double` | Two left clicks | The same, with `double` |
| `MDOWN left\|right\|middle` | Hold the button down. Later `MOVE` lines drag | `MDOWN <button>` and `MDOWN <button> done` |
| `MUP left\|right\|middle` | Release that button | `MUP <button>` and `MUP <button> done` |
| `SCROLL <steps>` | Vertical wheel. Positive is up, negative is down | `SCROLL <steps>` and `SCROLL done` |
| `HSCROLL <steps>` | Horizontal wheel. Positive is right, negative is left | `HSCROLL <steps>` and `HSCROLL done` |
| `TYPE <ascii>` | Type printable ASCII, from space (`0x20`) through `~` (`0x7E`). One space separates the verb; every space after that is typed | On success, it prints nothing. Otherwise `ERR TYPE bad` |
| `KEY <chord>` | Tap one key, with optional modifiers joined by `+` | `KEY <chord> done` or `ERR KEY bad` |
| `KDOWN <key>` | Hold a key down. The boot keyboard holds up to 6 keys at once | `KDOWN <key> done` or `ERR KDOWN bad` |
| `KUP <key>` | Release that key | `KUP <key> done` or `ERR KUP bad` |
| `HOTKEY <k1+k2+…>` | Press the steps in order, then release them in reverse. Up to 8 steps | `HOTKEY <canonical> done` or `ERR HOTKEY bad` |

`CLICK` leaves a button held by `MDOWN` still held.

`TYPE hello` types `hello`. `TYPE  hello` (two spaces) types a space and then `hello`. A byte outside that ASCII range, or an empty string, answers `ERR TYPE bad` and sends nothing.

`KEY` takes modifiers plus **one** key. A letter names the key, so `KEY a` taps `a`. The shifted character needs the modifier: `KEY shift+a`. The board confirms a chord in this order: `cmd`, `winright`, `ctrl`, `ctrlright`, `alt`, `altright`, `shift`, `shiftright`, then the key.

### Key names

Modifiers. The left column is what you can type. The right column is the name the board answers with.

| You type | It means |
|---|---|
| `cmd`, `command`, `meta`, `win`, `winleft`, `commandleft` | `cmd` (left Windows or Command key) |
| `cmdright`, `commandright`, `winright` | `winright` |
| `ctrl`, `control`, `ctrlleft` | `ctrl` |
| `ctrlright` | `ctrlright` |
| `alt`, `opt`, `option`, `altleft`, `optionleft` | `alt` |
| `altright`, `optionright` | `altright` |
| `shift`, `shiftleft` | `shift` |
| `shiftright` | `shiftright` |

Keys:

| Group | Names |
|---|---|
| Letters and digits | `a`–`z`, `0`–`9` |
| Function | `f1`–`f12` |
| Editing | `enter` (`return`), `esc` (`escape`), `backspace`, `tab`, `space`, `delete` (`del`), `insert` |
| Arrows | `left`, `right`, `up`, `down` |
| Navigation | `home`, `end`, `pageup` (`pgup`), `pagedown` (`pgdn`) |
| Punctuation | `minus`, `equal`, `leftbracket`, `rightbracket`, `backslash`, `semicolon`, `quote`, `grave`, `comma`, `dot`, `slash` |

A name outside that list answers `ERR KEY bad` (or `ERR KDOWN bad`, `ERR KUP bad`, `ERR HOTKEY bad`).

### Errors

| Reply | When |
|---|---|
| `ERR MOVE needs dx dy` | `dx` or `dy` is missing |
| `ERR CLICK left\|right\|double` | The button is something else |
| `ERR MDOWN left\|right\|middle` | The same, for `MDOWN` |
| `ERR MUP left\|right\|middle` | The same, for `MUP` |
| `ERR SCROLL needs steps` | The number is missing |
| `ERR HSCROLL needs steps` | The number is missing |
| `ERR TYPE bad` | Empty, a byte out of range, or the keyboard did not accept the report |
| `ERR KEY bad` | Empty chord, an extra key, or an unknown name |
| `ERR KDOWN bad`, `ERR KUP bad`, `ERR HOTKEY bad` | The argument could not be applied |
| `ERR line too long` | More than 95 characters; that line does not run |

### A short session

With a text editor focused:

```
STATUS
MOVE 40 0
MOVE -40 0
CLICK left
MDOWN left
MOVE 0 30
MUP left
SCROLL -1
TYPE hello
KEY enter
KEY cmd+a
HOTKEY ctrl+c
```

On macOS, `KEY cmd+a` selects all. `HOTKEY ctrl+c` copies. On Windows the system modifier is `win` (the board confirms it as `cmd`).

## A script that moves the pointer

[`examples/square.py`](examples/square.py) opens the port, sends four `MOVE` lines, and waits for `done` after each one. The pointer traces a square 60 counts on a side. Running it once performs the gesture once.

```sh
python3 -m pip install pyserial
python3 examples/square.py
# or, when more than one port is present:
python3 examples/square.py /dev/cu.usbmodem1101
```

```python
lines = ("MOVE 60 0", "MOVE 0 60", "MOVE -60 0", "MOVE 0 -60")
with serial.Serial(port, 115200, timeout=1) as link:
    time.sleep(0.3)
    link.reset_input_buffer()
    for line in lines:
        link.write((line + "\n").encode("ascii"))
        # read until the line that ends in "done"
```

The full file is in the repository. It looks for the port whose USB id is `2886:802F`, which is the sketch. `002F` is the bootloader, and it does not accept these commands.

To run it on a timer, use the scheduler you already have: `cron` on Linux and macOS, `launchd` on macOS, or Task Scheduler on Windows. The command is `python3` plus the path to the script.

## The same thing from Chrome

[`examples/square.html`](examples/square.html) talks to the board through the [Web Serial API](https://developer.mozilla.org/docs/Web/API/Web_Serial_API). Chrome and Edge have it. Serve the page over HTTP. A file opened as `file://` cannot request the port.

```sh
python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/examples/square.html` in Chrome. **Connect** picks the board (it filters USB vendor `0x2886`) and sends `STATUS`. **Move now** draws the square. **Every 15 seconds** repeats that gesture while the tab stays open. The `15000` in the file is the interval, in milliseconds.

Chrome asks for permission the first time. Keep a window in front where the pointer can move without clicking anything.

## Your own program

Any language that can open a serial port at 115200 can be the service that talks to the board. The board starts no gestures on its own: it runs the line it receives and answers on the same port.

The shape is always the same.

1. Find USB `2886:802F`.
2. Open it at 115200. Opening it prints the banner `=== LiveUse ===`.
3. Write a line ending in `\n`.
4. Read the reply. `MOVE`, `CLICK`, `SCROLL`, `KEY`, `KDOWN`, `KUP`, and `HOTKEY` finish with a line that ends in `done`. `TYPE`, on success, prints nothing. `STATUS` prints a single `OK …` line.

A minimal Python service, apart from the square:

```python
import time
import serial

link = serial.Serial("/dev/cu.usbmodem1101", 115200, timeout=1)
time.sleep(0.3)
link.reset_input_buffer()
link.write(b"STATUS\n")
print(link.readline().decode().strip())
link.close()
```

In Node the matching package is `serialport`. In the browser, the page above is already that client. From there you can send any command in the table: drag with `MDOWN` / `MOVE` / `MUP`, type with `TYPE`, or tap a shortcut with `KEY` and `HOTKEY`.

## The manifest, if a program will flash the board

`https://raw.githubusercontent.com/yortyrh/liveuse-releases/main/manifest.json` is the fixed URL of the latest version. `schema` is `1`. `version` is `major.minor.patch`. Each entry in `boards` describes one image.

For the SAMD21 the object carries:

- `url`, `sha256`, and `size`: the file and how to check it
- `usb.running`: `2886` / `802F`, the board with the sketch running
- `usb.bootloader`: `2886` / `002F`, the board waiting for the write
- `flash.protocol`: `sam-ba`
- `flash.enter`: `1200bps-touch` (open the CDC port at 1200 and close it), in addition to the double reset
- `flash.offset`: `0x2000`

`STATUS` reports the version already installed. When `version` in the manifest is newer and the connected USB id matches `usb.running`, that is the `.bin` to write, at the offset from the manifest itself.
