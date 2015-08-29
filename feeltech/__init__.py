# The MIT License (MIT)
# 
# Copyright (c) 2015 Josef Gajdusek
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import serial
import struct
from time import sleep

SINE = 0
SQUARE = 1
TRIANGLE = 2
ARB1 = 3
ARB2 = 4
ARB3 = 5
ARB4 = 6
ARB = [ARB1, ARB2, ARB3, ARB4]
LORENTZ = 7
MULTITONE = 8
RAND_NOISE = 9
ECG = 10
TRAPEZOID = 11
SINC = 12
NARROW = 13
GAUSS_NOISE = 14
AM = 15
FM = 16

LOG = 1
LINEAR = 2

class Channel:

    def __init__(self, i, ft):
        self._i = i
        self._ft = ft
        self._prefix = ("b" if i == 1 else "d")
        # TODO: Fetch the parameters for the main channel
        self._freq = None
        self._duty = None
        self._ampl = None
        self._off = None
        self._wf = None

    def waveform(self, w = None):
        if w == None:
            return self._wf
        else:
            self._wf = w
            cmd = self._prefix + "w%d" % w
            self._ft.send(cmd)
            return self

    def frequency(self, f = None):
        if f == None:
            return self._freq
        else:
            self._freq = f
            cmd = self._prefix + "f%d" % round(f * 100)
            self._ft.send(cmd)
            return self

    def duty(self, d = None):
        if d == None:
            return self._duty
        else:
            self._duty = d
            cmd = self._prefix + "d%d" % round(d * 10)
            self._ft.send(cmd)
            return self

    def amplitude(self, a = None):
        if a == None:
            return self._ampl
        else:
            self._ampl = a
            cmd = self._prefix + "a%2.1f" % a
            self._ft.send(cmd)
            return self

    def offset(self, o = None):
        if o == None:
            return self._off
        else:
            self._off = o
            cmd = self._prefix + "o%2.1f" % o
            self._ft.send(cmd)
            return self

    def start_sweep(self, freq_start, freq_end, time = 10, type = LINEAR):
        if self._i != 1:
            raise NotImplementedError("Sweep supported only on channel 1")
        self.stop_sweep()
        self.frequency(freq_start)
        self._ft.send("bs1")
        self.frequency(freq_end)
        self._ft.send("bs2")
        self._ft.send("bt%d" % time)
        self._ft.send("bm%d" % type)
        self._ft.send("br1")
        return self

    def stop_sweep(self):
        if self._i != 1:
            raise NotImplementedError("Sweep supported only on channel 1")
        self._ft.send("br0")
        return self

    def sleep(self, time):
        sleep(time)
        return self

class FeelTech:

    def __init__(self, sername):
        self._ser = serial.Serial(sername, 9600, timeout = 1)
        self._channels = [Channel(1, self), Channel(2, self)]
        self._phase = None

    def type(self):
        return self.exchange("a")

    def channels(self):
        return self._channels

    def send(self, command):
        if type(command) == str:
            command = command.encode("ascii")
        self._ser.write(command + b"\n")
        sleep(0.05)
        return self

    def exchange(self, command):
        self.send(command)
        ret = self._ser.readline()
        if ret == b"":
            raise TimeoutError()
        self._ser.flushInput()
        return ret[:-1].decode("ascii") # Ditch the newline

    def upload_waveform(self, i, data):
        self._ser.write(b"DDS_WAVE" + bytes([0xf0 + i]))
        r = self._ser.read(2)
        if r != b"SE":
            print(r)
            raise RuntimeError("Unexpected response when clearing waveform memory")

        self._ser.write(b"DDS_WAVE" + bytes([i]))
        r = self._ser.read(1)
        if r != b"W":
            raise RuntimeError("Unexpected response when writing waveform")

        for x in data:
            self._ser.write(struct.pack("<H", x))
            self._ser.read(2)
        self._ser.write(b"\n")
        r = self._ser.read(1)
        if r != b"N":
            raise RuntimeError("Unexpected response after writing waveform")
        return self

    def phase(self, p = None):
        if p == None:
            return self._phase
        else:
            self._phase = p
            self.send("dp%d" % p)
            return self

    def frequency(self):
        return int(self.exchange("ce")[2:]) * 10

    def counter(self):
        return int(self.exchange("cc")[2:])

    def clear_counter(self):
        self.send("bc")
        return self

    def sleep(self, time):
        sleep(time)
        return self

    def close(self):
        self._ser.close()
        return self
