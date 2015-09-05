# python-feeltech
Python library for controlling FeelTech FY32xx waveform generators

Install with

```
$ sudo pip3 install feeltech
```

## Library usage

To create FeelTech object

```
>>> import feeltech
>>> ft = feeltech.FeelTech("/dev/ttyUSB0")
>>> ft.type()
'FY3224S'
```

The two channels can then be accessed

```
>>> ft.channels()
[<feeltech.Channel object at 0x7f577b11fd10>, <feeltech.Channel object at 0x7f577b11fcd0>]
```

and to set various parameters

```
>>> c.frequency(30e3)
```

The calls can be chained like:

```
>>> c.frequency(30e3).amplitude(3.3)
```

Or even

```
>>> c.frequency(1e3).waveform(feeltech.SINE).sleep(3).waveform(feeltech.SQUARE)
```

To upload a waveform (decaying exponential):

```
>>> ft.upload_waveform(2, [int(e ** (-x / 1000) * 2 ** 12) for x in range(2048)])
>>> c.waveform(feeltech.ARB2)
```

![ds1054z-scope-display_2015-09-05_12-31-49](https://cloud.githubusercontent.com/assets/3966931/9698867/5316aea6-53ca-11e5-9fa5-effcb74e3c12.png)


## Commandline tool

```
$ fytool -h
usage: fytool [-h] [--port PORT] {type,set,sweep,frequency,counter,upload} ...

FeelTech FY32xx control utility

positional arguments:
  {type,set,sweep,frequency,counter,upload}
    type                display the device type
    set                 set channel properties
    sweep               Perform a frequency sweep
    frequency           Show frequency measured
    counter             Show counter value
    upload              upload arbitrary waveform

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  serial por
```

To set channel 1 frequency to 1 MHz, waveform to triangle and amplitude to 1V:

```
$ fytool set -c 1 -f 1e6 -w triangle -a 1
```

![ds1054z-scope-display_2015-09-05_12-44-45](https://cloud.githubusercontent.com/assets/3966931/9698904/188551be-53cc-11e5-9e44-564130314562.png)

Reading the internal frequency counter

```
$ fytool frequency
1000010
$ fytool counter
545269
```

To perform a loagrithmic sweep from 1 kHz to 10 kHz, with period of 1 second and lasting for total of 50 seconds:

```
fytool sweep -s 1e3 -e 10e3 --period 1 --time 50 --type log --waveform square
```

## TUI

There is also a curses interface to control the device

```
$ fytui /dev/ttyUSB0
```
![ds1054z-scope-display_2015-09-05_12-55-57](https://cloud.githubusercontent.com/assets/3966931/9698935/ae043a7e-53cd-11e5-8dc2-c09d6f370b9c.png)
![tui](https://cloud.githubusercontent.com/assets/3966931/9698931/a54afdfa-53cd-11e5-9791-76b25dc3e66f.png)

There is a bunch of keyboard shortcuts:

```
m     -- take frequency measurement
n     -- take counter measurement
w     -- focus waveform
f     -- focus frequency
d     -- focus duty cycle
a     -- focus amplitude
q     -- exit
+/s   -- increments selected digit
-/x   -- decremenets selected digit
```

For `w/f/d/a` if the control is already focused, it focuses its counterpart in the other channel.
